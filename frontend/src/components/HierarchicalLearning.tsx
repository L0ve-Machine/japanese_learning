import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  ListItemIcon,
  Breadcrumbs,
  Link,
  Card,
  CardContent,
  IconButton,
  Chip,
  LinearProgress,
  Drawer,
} from '@mui/material';
import {
  ArrowBack,
  Book,
  Chapter,
  Article,
  TextSnippet,
  NavigateNext,
  Menu,
  Close,
} from '@mui/icons-material';
import { Subject, SubjectItem, Chapter as ChapterType, Page, StudyText, Breadcrumb } from '../types';
import { learningService } from '../services/learning';

interface HierarchicalLearningProps {
  subject: Subject;
  onClose: () => void;
}

const HierarchicalLearning: React.FC<HierarchicalLearningProps> = ({
  subject,
  onClose
}) => {
  const [currentLevel, setCurrentLevel] = useState<'subject' | 'item' | 'chapter' | 'page' | 'text'>('subject');
  const [selectedItem, setSelectedItem] = useState<SubjectItem | null>(null);
  const [selectedChapter, setSelectedChapter] = useState<ChapterType | null>(null);
  const [selectedPage, setSelectedPage] = useState<Page | null>(null);
  const [selectedText, setSelectedText] = useState<StudyText | null>(null);
  const [breadcrumbs, setBreadcrumbs] = useState<Breadcrumb[]>([
    { id: subject.id, name: subject.name, type: 'subject' }
  ]);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  // Navigation handlers
  const navigateToItem = (item: SubjectItem) => {
    setSelectedItem(item);
    setCurrentLevel('item');
    setBreadcrumbs([
      ...breadcrumbs,
      { id: item.id, name: item.name, type: 'item' }
    ]);
  };

  const navigateToChapter = (chapter: ChapterType) => {
    setSelectedChapter(chapter);
    setCurrentLevel('chapter');
    setBreadcrumbs([
      ...breadcrumbs,
      { id: chapter.id, name: chapter.name, type: 'chapter' }
    ]);
  };

  const navigateToPage = (page: Page) => {
    setSelectedPage(page);
    setCurrentLevel('page');
    setBreadcrumbs([
      ...breadcrumbs,
      { id: page.id, name: page.name, type: 'page' }
    ]);
  };

  const navigateToText = (text: StudyText) => {
    setSelectedText(text);
    setCurrentLevel('text');
    setBreadcrumbs([
      ...breadcrumbs,
      { id: text.id, name: text.title, type: 'text' }
    ]);
  };

  // Breadcrumb navigation
  const navigateToBreadcrumb = (index: number) => {
    const targetBreadcrumb = breadcrumbs[index];
    const newBreadcrumbs = breadcrumbs.slice(0, index + 1);

    setBreadcrumbs(newBreadcrumbs);

    switch (targetBreadcrumb.type) {
      case 'subject':
        setCurrentLevel('subject');
        setSelectedItem(null);
        setSelectedChapter(null);
        setSelectedPage(null);
        setSelectedText(null);
        break;
      case 'item':
        setCurrentLevel('item');
        setSelectedChapter(null);
        setSelectedPage(null);
        setSelectedText(null);
        break;
      case 'chapter':
        setCurrentLevel('chapter');
        setSelectedPage(null);
        setSelectedText(null);
        break;
      case 'page':
        setCurrentLevel('page');
        setSelectedText(null);
        break;
    }
  };

  // Render different levels
  const renderSubjectItems = () => (
    <List>
      {subject.items?.map((item) => (
        <ListItem key={item.id} disablePadding>
          <ListItemButton onClick={() => navigateToItem(item)}>
            <ListItemIcon>
              <Book color="primary" />
            </ListItemIcon>
            <ListItemText
              primary={item.name}
              secondary={item.description}
            />
            <Chip
              label={`${item.chapters?.length || 0} 章`}
              size="small"
              color="primary"
              variant="outlined"
            />
          </ListItemButton>
        </ListItem>
      ))}
    </List>
  );

  const renderChapters = () => (
    <List>
      {selectedItem?.chapters?.map((chapter) => (
        <ListItem key={chapter.id} disablePadding>
          <ListItemButton onClick={() => navigateToChapter(chapter)}>
            <ListItemIcon>
              <Chapter color="secondary" />
            </ListItemIcon>
            <ListItemText
              primary={chapter.name}
              secondary={chapter.description}
            />
            <Chip
              label={`${chapter.pages?.length || 0} ページ`}
              size="small"
              color="secondary"
              variant="outlined"
            />
          </ListItemButton>
        </ListItem>
      ))}
    </List>
  );

  const renderPages = () => (
    <List>
      {selectedChapter?.pages?.map((page) => (
        <ListItem key={page.id} disablePadding>
          <ListItemButton onClick={() => navigateToPage(page)}>
            <ListItemIcon>
              <Article />
            </ListItemIcon>
            <ListItemText
              primary={page.name}
              secondary={page.description}
            />
            <Chip
              label={`${page.texts?.length || 0} テキスト`}
              size="small"
              variant="outlined"
            />
          </ListItemButton>
        </ListItem>
      ))}
    </List>
  );

  const renderTexts = () => (
    <List>
      {selectedPage?.texts?.map((text) => (
        <ListItem key={text.id} disablePadding>
          <ListItemButton onClick={() => navigateToText(text)}>
            <ListItemIcon>
              <TextSnippet />
            </ListItemIcon>
            <ListItemText
              primary={text.title}
              secondary={text.is_premium ? 'プレミアム' : '無料'}
            />
            {text.is_premium && (
              <Chip
                label="プレミアム"
                size="small"
                color="warning"
                variant="filled"
              />
            )}
          </ListItemButton>
        </ListItem>
      ))}
    </List>
  );

  const renderTextContent = () => (
    <Card>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          {selectedText?.title}
        </Typography>
        <Box
          dangerouslySetInnerHTML={{
            __html: selectedText?.content || ''
          }}
        />
      </CardContent>
    </Card>
  );

  const renderCurrentLevel = () => {
    switch (currentLevel) {
      case 'subject':
        return renderSubjectItems();
      case 'item':
        return renderChapters();
      case 'chapter':
        return renderPages();
      case 'page':
        return renderTexts();
      case 'text':
        return renderTextContent();
      default:
        return null;
    }
  };

  const getCurrentLevelTitle = () => {
    switch (currentLevel) {
      case 'subject':
        return `${subject.name} - 項目一覧`;
      case 'item':
        return `${selectedItem?.name} - 章一覧`;
      case 'chapter':
        return `${selectedChapter?.name} - ページ一覧`;
      case 'page':
        return `${selectedPage?.name} - テキスト一覧`;
      case 'text':
        return selectedText?.title || '';
      default:
        return '';
    }
  };

  return (
    <Container maxWidth="lg">
      {/* Header with breadcrumbs */}
      <Box sx={{ py: 2, display: 'flex', alignItems: 'center', gap: 2 }}>
        <IconButton onClick={onClose}>
          <ArrowBack />
        </IconButton>

        <Box sx={{ flexGrow: 1 }}>
          <Breadcrumbs separator={<NavigateNext fontSize="small" />}>
            {breadcrumbs.map((breadcrumb, index) => (
              <Link
                key={`${breadcrumb.type}-${breadcrumb.id}`}
                color="inherit"
                href="#"
                onClick={(e) => {
                  e.preventDefault();
                  navigateToBreadcrumb(index);
                }}
                sx={{
                  textDecoration: 'none',
                  '&:hover': { textDecoration: 'underline' }
                }}
              >
                {breadcrumb.name}
              </Link>
            ))}
          </Breadcrumbs>

          <Typography variant="h4" sx={{ mt: 1 }}>
            {getCurrentLevelTitle()}
          </Typography>
        </Box>

        <IconButton onClick={() => setDrawerOpen(true)}>
          <Menu />
        </IconButton>
      </Box>

      {/* Loading indicator */}
      {loading && <LinearProgress sx={{ mb: 2 }} />}

      {/* Main content */}
      <Box>
        {renderCurrentLevel()}
      </Box>

      {/* Navigation drawer for mobile */}
      <Drawer
        anchor="right"
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
      >
        <Box sx={{ width: 300, p: 2 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6">ナビゲーション</Typography>
            <IconButton onClick={() => setDrawerOpen(false)}>
              <Close />
            </IconButton>
          </Box>

          <List>
            {breadcrumbs.map((breadcrumb, index) => (
              <ListItem key={`nav-${breadcrumb.type}-${breadcrumb.id}`} disablePadding>
                <ListItemButton
                  onClick={() => {
                    navigateToBreadcrumb(index);
                    setDrawerOpen(false);
                  }}
                  selected={index === breadcrumbs.length - 1}
                >
                  <ListItemText primary={breadcrumb.name} />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
        </Box>
      </Drawer>
    </Container>
  );
};

export default HierarchicalLearning;