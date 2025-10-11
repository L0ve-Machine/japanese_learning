# Django Admin Inline Implementation Guide

## ⚠️ IMPORTANT DECISION NEEDED ⚠️

**🔴 CRITICAL QUESTION TO RESOLVE:**

**Will there be multiple Pages per Chapter, or just ONE Page per Chapter?**

This decision affects:
- Database structure efficiency
- Admin workflow complexity
- How content is organized and displayed
- Whether we need the Page model at all

**Current structure:**
```
Subject → Item → Chapter → Page (← Do we need this level?)
                           └── TextBlocks, Quizzes
```

**Option A:** Multiple pages per chapter (current setup)
- Keep Page model
- More flexible content organization
- Each page = one lesson/topic

**Option B:** One page per chapter (simpler)
- Remove Page model
- Chapter directly contains TextBlocks & Quizzes
- Simpler admin, fewer clicks

**👉 REMINDER: Discuss this decision before proceeding with nested admin implementation!**

---

## Project Context

**Project:** Japanese Learning App - 介護福祉士試験対策
**Goal:** Simplify admin data entry by adding inline forms to edit related models on the same page
**File to modify:** `backend/apps/learning/admin.py`

## Current Database Structure

```
Subject (科目)
  └── SubjectItem (項目)
       └── Chapter (章)
            └── Page (ページ)
                 ├── TextBlock (テキストブロック)
                 │    └── VocabularyEntry (語彙) ✓ Already has inline
                 └── QuizQuestion (クイズ問題)
                      └── QuizOption (選択肢) ✓ Already has inline
```

## Current Database Content (as of 2025-10-09)

- **5 Subjects**
- **9 Items**
- **13 Chapters**
- **13 Pages**
- **4 Text Blocks** (only in 介護保険 Chapter 1)
- **2 Quiz Questions** (only in 介護保険 Chapter 1)

**Issue:** 12 out of 13 pages are empty and need content.

## Existing Inlines (Already Implemented)

1. ✓ `VocabularyEntryInline` in `TextBlockAdmin` (line 133-136)
2. ✓ `QuizOptionInline` in `QuizQuestionAdmin` (line 157-160)

## Proposed Implementation Plan

### Priority 1: PageAdmin - Add Content Inlines (MOST IMPORTANT)

**Goal:** Allow creating Page + TextBlocks + QuizQuestions in one form

**Add these inline classes:**

```python
class TextBlockInline(admin.TabularInline):
    model = TextBlock
    extra = 2  # Show 2 empty forms by default
    fields = ['japanese_text', 'indonesian_translation', 'order']
    ordering = ['order']

class QuizQuestionInline(admin.StackedInline):
    model = QuizQuestion
    extra = 1  # Show 1 empty form by default
    fields = ['question_number', 'question_text', 'order']
    ordering = ['order']
```

**Modify PageAdmin to include inlines:**

```python
@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['name', 'chapter', 'get_item', 'get_subject', 'order', 'is_active']
    list_filter = ['is_active', 'chapter__item__subject']
    search_fields = ['name', 'description']
    ordering = ['chapter__item__subject', 'chapter__item__order', 'chapter__order', 'order']
    inlines = [TextBlockInline, QuizQuestionInline]  # ← ADD THIS LINE

    def get_item(self, obj):
        return obj.chapter.item.name
    get_item.short_description = 'Item'

    def get_subject(self, obj):
        return obj.chapter.item.subject.name
    get_subject.short_description = 'Subject'
```

**Result:**
- Create pages with multiple text blocks in one form
- Add quiz questions (but not their options - need to edit quiz separately)
- Saves ~5 page navigations per page

**Limitation:**
- Cannot add QuizOptions inline (would need nested admin for that)
- Vocabulary still needs to be added via TextBlock edit page

### Priority 2 (Optional): ChapterAdmin - Add Page Inline

**Goal:** Create Chapter + all Pages at once

```python
class PageInline(admin.TabularInline):
    model = Page
    extra = 3
    fields = ['name', 'description', 'order', 'is_active']
    ordering = ['order']
    show_change_link = True  # Adds link to edit full page with content

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['name', 'item', 'get_subject', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'item__subject']
    search_fields = ['name', 'description']
    ordering = ['item__subject', 'item__order', 'order', 'name']
    inlines = [PageInline]  # ← ADD THIS LINE

    def get_subject(self, obj):
        return obj.item.subject.name
    get_subject.short_description = 'Subject'
```

**Result:** Create chapter structure quickly, then add content to each page

### Priority 3 (Optional): SubjectItemAdmin - Add Chapter Inline

**Goal:** Create Item + Chapters at once

```python
class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 2
    fields = ['name', 'description', 'order', 'is_active']
    ordering = ['order']
    show_change_link = True

@admin.register(SubjectItem)
class SubjectItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'subject']
    search_fields = ['name', 'description']
    ordering = ['subject', 'order', 'name']
    inlines = [ChapterInline]  # ← ADD THIS LINE
```

## Implementation Steps

1. **Backup admin.py**
   ```bash
   cd backend/apps/learning
   cp admin.py admin.py.backup
   ```

2. **Add inline classes** (before the admin classes that use them)
   - Add `TextBlockInline` and `QuizQuestionInline` before `PageAdmin`
   - Add `PageInline` before `ChapterAdmin` (if implementing Priority 2)
   - Add `ChapterInline` before `SubjectItemAdmin` (if implementing Priority 3)

3. **Modify admin classes** to include `inlines = [...]`

4. **Test in admin interface**
   - Visit http://127.0.0.1:8000/admin/learning/page/add/
   - Verify inline forms appear
   - Test creating page with text blocks

5. **Restart server if needed** (Django usually auto-reloads admin.py changes)

## Alternative: Nested Admin (Advanced) - RECOMMENDED APPROACH

For full nested support (e.g., add QuizOptions when creating QuizQuestion inline):

### What is Nested Admin?

**Nested Admin** allows you to edit multiple levels of related models on a single page. This means:
- Edit Page → TextBlocks → Vocabulary (all on one page)
- Edit Page → QuizQuestions → Options with explanations (all on one page)

### Installation Steps

1. **Install package:**
   ```bash
   pip install django-nested-admin
   ```

2. **Add to `backend/core/settings.py`:**
   ```python
   INSTALLED_APPS = [
       ...
       'nested_admin',  # Add this line
   ]
   ```

3. **Run migrations (if needed):**
   ```bash
   python manage.py migrate
   ```

### Implementation Example

**Full implementation in `backend/apps/learning/admin.py`:**

```python
import nested_admin

# Innermost level - Vocabulary within TextBlock
class VocabularyEntryNestedInline(nested_admin.NestedTabularInline):
    model = VocabularyEntry
    extra = 1
    fields = ['japanese_word', 'indonesian_translation', 'order']
    ordering = ['order']

# Second level - TextBlock within Page
class TextBlockNestedInline(nested_admin.NestedStackedInline):
    model = TextBlock
    inlines = [VocabularyEntryNestedInline]  # Nested vocabulary
    extra = 1
    fields = ['japanese_text', 'indonesian_translation', 'order']
    ordering = ['order']

# Innermost level - QuizOption within QuizQuestion
class QuizOptionNestedInline(nested_admin.NestedTabularInline):
    model = QuizOption
    extra = 5  # Show 5 option slots by default
    fields = ['option_number', 'option_text', 'is_correct', 'explanation_japanese', 'explanation_indonesian']
    ordering = ['option_number']

# Second level - QuizQuestion within Page
class QuizQuestionNestedInline(nested_admin.NestedStackedInline):
    model = QuizQuestion
    inlines = [QuizOptionNestedInline]  # Nested options
    extra = 1
    fields = ['question_number', 'question_text', 'order']
    ordering = ['order']

# Top level - Page with everything nested
@admin.register(Page)
class PageAdmin(nested_admin.NestedModelAdmin):  # Note: NestedModelAdmin instead of ModelAdmin
    list_display = ['name', 'chapter', 'get_item', 'get_subject', 'order', 'is_active']
    list_filter = ['is_active', 'chapter__item__subject']
    search_fields = ['name', 'description']
    ordering = ['chapter__item__subject', 'chapter__item__order', 'chapter__order', 'order']
    inlines = [TextBlockNestedInline, QuizQuestionNestedInline]  # Both nested inlines

    def get_item(self, obj):
        return obj.chapter.item.name
    get_item.short_description = 'Item'

    def get_subject(self, obj):
        return obj.chapter.item.subject.name
    get_subject.short_description = 'Subject'
```

### What You'll See in Admin

**Before (standard approach):**
- Page → TextBlock (separate page) → Vocabulary (separate page)
- Page → QuizQuestion (separate page) → QuizOption (separate page)
- Total: ~15+ page navigations

**After (nested admin):**
```
┌─────────────────────────────────────────────────────┐
│ Add Page: "介護保険制度とは？"                       │
├─────────────────────────────────────────────────────┤
│ Name: [___________]                                 │
│ Chapter: [介護保険 - 第1章 ▼]                      │
│                                                     │
│ ━━━ TEXT BLOCKS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                     │
│ ▼ Text Block #1                                    │
│   Japanese: [介護保険は高齢者の...]                │
│   Indonesian: [Asuransi perawatan adalah...]       │
│                                                     │
│   ┌─ Vocabulary ────────────────────────────┐     │
│   │ Word        Translation        Order    │     │
│   │ [介護]      [perawatan]        [1]      │     │
│   │ [高齢者]    [lansia]           [2]      │     │
│   │ + Add vocabulary                        │     │
│   └─────────────────────────────────────────┘     │
│                                                     │
│ + Add text block                                   │
│                                                     │
│ ━━━ QUIZ QUESTIONS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                     │
│ ▼ Question #1                                      │
│   Question: [介護保険の目的は？]                   │
│                                                     │
│   ┌─ Options ─────────────────────────────┐       │
│   │ #  Text              ✓  Explanation JP/ID │   │
│   │ 1  [高齢者の支援]   ☑  [説明...][...]     │   │
│   │ 2  [若者の支援]     ☐  [説明...][...]     │   │
│   │ 3  [...]            ☐  [説明...][...]     │   │
│   │ 4  [...]            ☐  [説明...][...]     │   │
│   │ 5  [...]            ☐  [説明...][...]     │   │
│   │ + Add option                              │   │
│   └───────────────────────────────────────────┘   │
│                                                     │
│ + Add question                                     │
│                                                     │
│ [Save]                                             │
└─────────────────────────────────────────────────────┘
```

### Pros and Cons

**Pros:**
✓ Everything on one page - matches your desired workflow exactly
✓ Add text with vocabulary words that trigger translations
✓ Add quiz questions with all options and explanations inline
✓ Drag-and-drop reordering (optional feature)
✓ Collapsible sections to reduce clutter
✓ Saves 10+ clicks per page
✓ Popular, well-maintained package (1M+ downloads)

**Cons:**
✗ Additional dependency (django-nested-admin)
✗ Slightly more complex form (but organized)
✗ Page loads slightly slower with many nested items
✗ Requires ~10-15 min initial setup

### Files Modified

1. **`backend/requirements.txt`** - Add `django-nested-admin`
2. **`backend/core/settings.py`** - Add to INSTALLED_APPS
3. **`backend/apps/learning/admin.py`** - Update inline classes and PageAdmin

**Total changes:** ~50-60 lines in admin.py

### What DOESN'T Change

✓ Database structure - no migrations needed (just run migrate for nested_admin tables)
✓ Models - no changes
✓ Frontend - no changes
✓ API - no changes
✓ Existing data - all stays intact

### Reversibility

**To rollback:**
1. Remove `'nested_admin'` from INSTALLED_APPS
2. Restore `admin.py` from backup
3. Uninstall: `pip uninstall django-nested-admin`
4. Everything returns to normal

### Performance Impact

- **Form loading:** +0.5-1 second (negligible for your data size)
- **Saving:** Same speed
- **Database:** More efficient (uses prefetch_related)

### Security & Maintenance

- **Package:** `django-nested-admin`
- **Maintained:** Yes (active development)
- **Downloads:** 1M+ monthly
- **Django support:** Supports Django 3.2 - 5.0+
- **Last update:** Recent (check PyPI)

### Visual Enhancements

Nested admin includes:
- JavaScript for dynamic adding/removing
- Collapsible sections (▼/▶ arrows)
- Visual indentation for hierarchy
- Inline validation
- Improved UX for complex forms

## Recommended Approach - USER REQUIREMENTS

### Two-Group Strategy

The admin will be divided into **TWO NESTED GROUPS:**

---

### **GROUP 1: Structure/Outline (Subject → Item → Chapter → Page)**

✅ **SubjectAdmin - CREATE FULL STRUCTURE:**
- Subject details
- → Items inline (nested level 1)
  - → Chapters inline (nested level 2)
    - → Pages inline (nested level 3)

**Purpose:** Create the entire course outline/skeleton in one page

**What you get:**
```
One form to create:
- Subject: 介護保険対策
  - Item 1: 介護保険
    - Chapter 1: 第1章 - 概要
      - Page 1.1: 介護保険制度とは？
      - Page 1.2: 制度の目的
    - Chapter 2: 第2章 - 被保険者
      - Page 2.1: 被保険者について
  - Item 2: 給付の種類
    - Chapter 1: ...
```

**Result:** Entire structure created in **1 page** instead of 20+ clicks

---

### **GROUP 2: Content/Details (Page → Blocks → Quizzes)**

✅ **PageAdmin - ADD ALL CONTENT:**
- Text blocks inline (nested level 1)
  - → Vocabulary inline (nested level 2)
- Quiz questions inline (nested level 1)
  - → Quiz options + explanations inline (nested level 2)

**Purpose:** Fill in the actual learning content for each page

**What you get:**
```
Edit a page to add:
- Multiple text blocks with Japanese/Indonesian translations
  - Vocabulary words for each text block
- Multiple quiz questions
  - 5 options per quiz with explanations (JP/ID)
```

**Result:** All content for a page created in **1 page**

---

### Implementation Plan

**Implement TWO nested admin sections:**

1. **SubjectAdmin (Structure):**
   - Subject → Items → Chapters → Pages (4 levels deep)
   - Just names/order, no content

2. **PageAdmin (Content):**
   - Page → TextBlocks → Vocabulary
   - Page → QuizQuestions → Options with explanations

---

### Workflow

**Phase 1: Plan the course structure**
1. Go to Subjects → Add Subject
2. Add all Items, Chapters, and Pages in one nested form
3. Save → Entire outline is created

**Phase 2: Fill in the content**
1. Go to Pages → Select a page
2. Add text blocks with vocabulary
3. Add quiz questions with options and explanations
4. Save → Page is complete

**Benefits:**
- Clear separation: Planning vs Content creation
- Maximum efficiency: Each phase = 1 page
- Easy to reorganize structure before adding content
- Can see full outline at a glance

---

### Visual Preview

**GROUP 1 - Structure Creation:**
```
┌─ Add Subject ──────────────────────────────┐
│ Name: [介護保険対策]                        │
│                                             │
│ ▼ Items                                    │
│   ├─ Item: [介護保険]                      │
│   │   ▼ Chapters                           │
│   │     ├─ Chapter: [第1章] Order: [1]    │
│   │     │   ▼ Pages                        │
│   │     │     ├─ Page: [1. 制度とは] [1]  │
│   │     │     └─ Page: [2. 目的] [2]      │
│   │     └─ Chapter: [第2章] Order: [2]    │
│   │         ▼ Pages                        │
│   │           └─ Page: [被保険者] [1]     │
│   └─ + Add item                            │
│                                             │
│ [Save Structure]                           │
└─────────────────────────────────────────────┘
```

**GROUP 2 - Content Addition:**
```
┌─ Edit Page: "1. 介護保険制度とは？" ────────┐
│                                             │
│ ▼ Text Blocks                              │
│   ├─ Block 1:                              │
│   │   Japanese: [介護保険は...]            │
│   │   Indonesian: [Asuransi...]            │
│   │   ▼ Vocabulary                         │
│   │     ├─ [介護] → [perawatan]           │
│   │     └─ [高齢者] → [lansia]            │
│   └─ + Add text block                     │
│                                             │
│ ▼ Quiz Questions                           │
│   └─ Question 1: [目的は？]                │
│       ▼ Options                            │
│         ├─ 1. [高齢者支援] ☑ + explanation │
│         ├─ 2. [若者支援] ☐ + explanation   │
│         └─ (3-5...)                        │
│                                             │
│ [Save Content]                             │
└─────────────────────────────────────────────┘
```

## Testing Checklist

After implementation:

- [ ] Can create new page with multiple text blocks inline
- [ ] Can add quiz questions inline
- [ ] Can edit existing pages and see existing text blocks
- [ ] Order field works correctly
- [ ] Can delete inline items
- [ ] No errors in Django admin
- [ ] Server starts without errors

## Rollback Plan

If something breaks:
```bash
cd backend/apps/learning
cp admin.py.backup admin.py
python manage.py check
python manage.py runserver
```

## Related Files

- Main file: `backend/apps/learning/admin.py`
- Models: `backend/apps/learning/models.py`
- Reference doc: `科目学習 datamanagement.txt`

## Server Commands

```bash
# Start server
cd backend && python manage.py runserver

# Check for errors
python manage.py check

# Access admin
http://127.0.0.1:8000/admin/
```

## Notes

- Inline forms appear when creating OR editing the parent object
- `extra = N` controls how many blank forms show by default
- `show_change_link = True` adds a link to edit the full object
- `TabularInline` = compact table view
- `StackedInline` = vertical form view (better for long text fields)
- Inlines use the same permissions as the parent model

## Next Steps After Implementation

1. Test by adding content to the 12 empty pages
2. Consider building CSV/Excel import if inline still too slow
3. Document the new workflow for content creators

---

# Frontend UI Automation

## Current Situation

**Backend:** Django admin with nested inlines for content management
**Frontend:** User-facing website that displays subjects/chapters/pages
**API:** REST API at `/api/learning/subjects/` that provides all data

## Problem: Manual Frontend Development

Currently, when you add new subjects via admin:
1. ✅ Backend: Data is saved to database
2. ✅ API: Data is available via `/api/learning/subjects/`
3. ❌ Frontend: **UI must be manually created** in HTML/JavaScript

**This means:**
- Add "介護保険" subject in admin → Works
- Add chapters/pages in admin → Works
- But frontend HTML must be manually coded to display it

## Goal: Automate Frontend UI Generation

**Desired workflow:**
1. Create subject structure in admin (Subject → Items → Chapters → Pages)
2. Add content in admin (Text blocks, vocabulary, quizzes)
3. **Frontend automatically generates UI pages** without manual coding

## Options for Automation

### Option 1: Dynamic Frontend (Recommended)

**Approach:** Frontend fetches structure from API and renders dynamically

**Implementation:**
```javascript
// Fetch subjects from API
fetch('/api/learning/subjects/')
  .then(res => res.json())
  .then(subjects => {
    // Automatically generate navigation
    subjects.forEach(subject => {
      createSubjectPage(subject);
      subject.items.forEach(item => {
        createItemPage(item);
        item.chapters.forEach(chapter => {
          createChapterPage(chapter);
          chapter.pages.forEach(page => {
            createContentPage(page);
          });
        });
      });
    });
  });
```

**Pros:**
- No manual HTML needed
- New subjects appear automatically
- Frontend stays in sync with admin
- One template handles all pages

**Cons:**
- Requires JavaScript framework (React, Vue, etc.)
- More complex initial setup
- SEO might need server-side rendering

**Files needed:**
- `frontend/js/dynamic-subject-loader.js` - Fetches and renders subjects
- `frontend/templates/subject-template.html` - Reusable template
- `frontend/css/subject-styles.css` - Styling

### Option 2: Static Site Generator

**Approach:** Generate static HTML files from database on demand

**Implementation:**
```python
# Django management command
python manage.py generate_frontend_pages

# This creates:
# frontend/subjects/kaigohoken/index.html
# frontend/subjects/kaigohoken/chapter-1.html
# etc.
```

**Pros:**
- Fast loading (static HTML)
- Good for SEO
- No JavaScript required
- Can version control generated files

**Cons:**
- Must regenerate after admin changes
- More storage (duplicate data)
- Extra build step

**Files needed:**
- `backend/apps/learning/management/commands/generate_pages.py`
- `backend/templates/subject_template.html` (Jinja2 template)

### Option 3: Hybrid - Template Components

**Approach:** Use Django template tags to auto-generate HTML

**Implementation:**
```django
{# subjects.html #}
{% load learning_tags %}

{% get_all_subjects as subjects %}
{% for subject in subjects %}
  {% render_subject subject %}
{% endfor %}
```

**Pros:**
- Server-side rendering (good SEO)
- Automatic updates
- No build step
- Simple to implement

**Cons:**
- Still tied to Django views
- Less dynamic than pure JavaScript
- Harder to make interactive

**Files needed:**
- `backend/apps/learning/templatetags/learning_tags.py`
- `backend/templates/components/subject_card.html`
- `backend/templates/components/chapter_list.html`

### Option 4: Headless CMS Approach

**Approach:** Treat Django as pure API, use modern frontend framework

**Stack:**
- Backend: Django REST API (already have this)
- Frontend: Next.js / Nuxt.js / SvelteKit
- Data: Fetched from `/api/learning/subjects/`

**Implementation:**
```javascript
// Next.js pages/subjects/[slug].js
export async function getServerSideProps({ params }) {
  const subject = await fetch(`/api/learning/subjects/${params.slug}/`);
  return { props: { subject } };
}

export default function SubjectPage({ subject }) {
  return <SubjectLayout subject={subject} />;
}
```

**Pros:**
- Modern, fast, interactive
- Automatic routing
- Great developer experience
- Best SEO with SSR

**Cons:**
- Requires learning new framework
- More complex setup
- Separate deployment

## Recommended Approach

**For your use case: Option 1 (Dynamic Frontend) or Option 3 (Hybrid)**

### Quick Implementation (Option 3 - Template Tags)

**Step 1:** Create template tags

```python
# backend/apps/learning/templatetags/learning_tags.py
from django import template
from apps.learning.models import Subject

register = template.Library()

@register.simple_tag
def get_all_subjects():
    return Subject.objects.filter(is_active=True).prefetch_related(
        'items__chapters__pages'
    )

@register.inclusion_tag('components/subject_navigation.html')
def render_subject_nav(subject):
    return {'subject': subject}
```

**Step 2:** Create reusable component

```html
<!-- backend/templates/components/subject_navigation.html -->
<div class="subject-nav">
  <h2>{{ subject.name }}</h2>
  <ul>
    {% for item in subject.items.all %}
      <li>
        <a href="{% url 'item_detail' subject.id item.id %}">
          {{ item.name }}
        </a>
        <ul>
          {% for chapter in item.chapters.all %}
            <li>
              <a href="{% url 'chapter_detail' subject.id item.id chapter.id %}">
                {{ chapter.name }}
              </a>
            </li>
          {% endfor %}
        </ul>
      </li>
    {% endfor %}
  </ul>
</div>
```

**Step 3:** Use in templates

```html
<!-- backend/templates/subjects/index.html -->
{% load learning_tags %}

<div class="subjects-container">
  {% get_all_subjects as subjects %}
  {% for subject in subjects %}
    {% render_subject_nav subject %}
  {% endfor %}
</div>
```

**Result:**
- Add subject in admin → Automatically appears in frontend
- No manual HTML coding needed
- One template handles all subjects

## Implementation Checklist

### For Template Tag Approach (Recommended)

- [ ] Create `templatetags` directory in `apps/learning/`
- [ ] Create `learning_tags.py` with subject fetching logic
- [ ] Create component templates in `templates/components/`
- [ ] Update views to use new templates
- [ ] Add CSS styling for generated components
- [ ] Test with existing subjects
- [ ] Verify new subjects appear automatically

### For Dynamic JavaScript Approach

- [ ] Create `frontend/js/api-client.js` for API calls
- [ ] Create `frontend/js/subject-renderer.js` for dynamic rendering
- [ ] Create HTML templates (can use `<template>` tags)
- [ ] Add event listeners for navigation
- [ ] Implement routing (hash-based or History API)
- [ ] Add loading states and error handling
- [ ] Test with different subjects/chapters

## API Endpoints Available

Already implemented in `backend/apps/learning/views.py`:

```
GET /api/learning/subjects/                  # List all subjects
GET /api/learning/subjects/{id}/             # Subject details with hierarchy
GET /api/learning/subjects/{id}/hierarchy/   # Full nested structure
GET /api/learning/items/{id}/chapters/       # Chapters for an item
GET /api/learning/chapters/{id}/pages/       # Pages for a chapter
GET /api/learning/pages/{id}/texts/          # Texts for a page
```

**All endpoints:**
- Return nested data
- Filter by `is_active=True`
- Support prefetching (efficient queries)
- Include Indonesian translations

## Example: Auto-Generated Page Structure

**When you create this in admin:**
```
Subject: 介護保険対策
  └── Item: 介護保険
       └── Chapter: 第1章 - 概要
            └── Page: 1. 介護保険制度とは
                 ├── TextBlock: "介護保険は..."
                 │    └── Vocab: 介護 → perawatan
                 └── Quiz: "介護保険の目的は？"
                      └── Options: [5 choices]
```

**Frontend auto-generates:**
```html
<div class="subject" data-id="1">
  <h1>介護保険対策</h1>
  <div class="item" data-id="1">
    <h2>介護保険</h2>
    <div class="chapter" data-id="1">
      <h3>第1章 - 概要</h3>
      <div class="page" data-id="1">
        <h4>1. 介護保険制度とは</h4>
        <div class="text-block">
          <p>介護保険は...</p>
          <div class="vocabulary">
            <span class="word" data-translation="perawatan">介護</span>
          </div>
        </div>
        <div class="quiz">
          <p>介護保険の目的は？</p>
          <form class="quiz-options">
            <!-- 5 auto-generated options -->
          </form>
        </div>
      </div>
    </div>
  </div>
</div>
```

## Next Action

**Decision needed:** Which automation approach do you want to implement?

1. **Template Tags** (simpler, server-side) - Good for getting started
2. **Dynamic JavaScript** (more flexible, client-side) - Good for interactivity
3. **Modern Framework** (most powerful, requires learning) - Best long-term

Once you choose, we can implement the automation system.
