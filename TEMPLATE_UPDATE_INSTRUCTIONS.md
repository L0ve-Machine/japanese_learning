# Template Update Instructions - Dynamic Subject Loading

## Overview

This guide explains how to update the `subject_learning.html` template to dynamically load subjects from the database instead of showing hardcoded cards.

## Current Problem

The template at `backend/templates/subjects/subject_learning.html` has **hardcoded HTML** for 5 specific subjects (lines 390-603). Even though the view passes `subjects` from the database, the template ignores this variable.

**Result**: New subjects created in admin don't appear on http://127.0.0.1:8000/subjects/

## What Needs to Change

### Before (Hardcoded - lines 390-603):
```html
<div class="subjects-grid">
    <!-- Subject 1: 介護試験対策 -->
    <div class="subject-card">
        <div class="card-icon" style="background: #4caf50;">
            <span class="material-icons">medical_services</span>
        </div>
        <div class="card-title">介護試験対策</div>
        ...
    </div>

    <!-- Subject 2: 介護の実務会話 -->
    <div class="subject-card">
        ...
    </div>

    <!-- ... 3 more hardcoded cards ... -->
</div>
```

### After (Dynamic):
```html
<div class="subjects-grid">
    {% for subject in subjects %}
    <div class="subject-card">
        <div class="card-icon" style="background: {{ subject.color }};">
            <span class="material-icons">{{ subject.icon }}</span>
        </div>
        <div class="card-title">{{ subject.name }}</div>
        <div class="card-description">{{ subject.indonesian_name }}</div>
        ...
        <div class="stat-value">{{ subject.items.count }}</div>
        ...
        <button onclick="startLearning('{{ subject.name|escapejs }}')">
            学習開始
        </button>
    </div>
    {% empty %}
    <div class="no-results" style="display: block;">
        <h3>科目がまだ登録されていません</h3>
        <p>管理画面で科目を追加してください</p>
    </div>
    {% endfor %}
</div>
```

## Template Variables Available

The view `subject_learning_view` provides:
- `subjects` - QuerySet of all active Subject objects
- `user` - Current user

Each `subject` object has:
- `subject.name` - Japanese name
- `subject.indonesian_name` - Indonesian name
- `subject.description` - Description text
- `subject.icon` - Material icon name (e.g., 'medical_services')
- `subject.color` - Hex color code (e.g., '#4caf50')
- `subject.items.count` - Number of items
- `subject.items.all` - All items (for counting chapters)

## Detailed Implementation Steps

### Step 1: Locate the Hardcoded Section
**File**: `backend/templates/subjects/subject_learning.html`
**Lines**: 389-604

Look for:
```html
<!-- Subjects Grid -->
<div class="subjects-grid" id="subjectsGrid">
    <!-- Subject 1: 介護試験対策 -->
```

### Step 2: Replace with Django Loop

**Delete lines 390-603** (all hardcoded subject cards)

**Replace with**:
```django
<!-- Subjects Grid -->
<div class="subjects-grid" id="subjectsGrid">
    {% for subject in subjects %}
    <!-- Subject: {{ subject.name }} -->
    <div class="subject-card" data-subject-id="{{ subject.id }}">
        <div class="card-header">
            <div class="card-icon" style="background: {{ subject.color }};">
                <span class="material-icons">{{ subject.icon }}</span>
            </div>
            <div>
                <div class="card-title">{{ subject.name }}</div>
                <div class="card-description">{{ subject.indonesian_name|default:subject.description }}</div>
            </div>
        </div>

        <div class="progress-section">
            <div class="progress-header">
                <span class="progress-label">学習進捗</span>
                <span class="progress-label">0%</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: 0%; background: {{ subject.color }};"></div>
            </div>
        </div>

        <div class="stats-row">
            <div class="stat-item">
                <div class="stat-value">{{ subject.items.count }}</div>
                <div class="stat-label">項目</div>
            </div>
            <div class="stat-item">
                {% with total_chapters=0 %}
                    {% for item in subject.items.all %}
                        {% with total_chapters=total_chapters|add:item.chapters.count %}{% endwith %}
                    {% endfor %}
                    <div class="stat-value">{{ total_chapters }}</div>
                {% endwith %}
                <div class="stat-label">章</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{% if subject.items.count > 0 %}進行中{% else %}準備中{% endif %}</div>
                <div class="stat-label">状態</div>
            </div>
        </div>

        <button class="action-btn btn-primary" style="background: {{ subject.color }};" onclick="startLearning('{{ subject.name|escapejs }}')">
            <span class="material-icons">play_arrow</span>
            学習開始
        </button>
    </div>
    {% empty %}
    <!-- No subjects message -->
    <div class="no-results" style="display: block;">
        <span class="material-icons" style="font-size: 48px; color: #ccc; margin-bottom: 16px;">folder_open</span>
        <h3>科目がまだ登録されていません</h3>
        <p>管理画面で科目を追加してください</p>
    </div>
    {% endfor %}
</div>
```

### Step 3: Optional - Fix Chapter Count (Simplified)

The chapter count calculation above is complex. For a simpler version, update the view to calculate it:

**File**: `backend/apps/web/views.py`

Find `subject_learning_view` and modify:
```python
def subject_learning_view(request):
    """科目学習メインページ - Load subjects from database"""
    from apps.learning.models import Subject

    # Get all active subjects from database with prefetch
    subjects = Subject.objects.filter(is_active=True).prefetch_related(
        'items__chapters'
    ).order_by('order')

    # Add chapter count to each subject
    for subject in subjects:
        subject.total_chapters = sum(item.chapters.count() for item in subject.items.all())

    return render(request, 'subjects/subject_learning.html', {
        'subjects': subjects,
        'user': request.user
    })
```

Then in template use:
```django
<div class="stat-value">{{ subject.total_chapters }}</div>
```

### Step 4: Keep the "No Results" Section

Make sure to keep the existing no-results div (currently at line 607-611) but it should only show when search returns 0 results. The `{% empty %}` block handles when there are no subjects in the database.

## Testing

### Test 1: Verify All Existing Subjects Appear
1. Navigate to http://127.0.0.1:8000/subjects/
2. You should see 6 subject cards (including "testing")
3. Each should have:
   - Correct icon from database
   - Correct color from database
   - Japanese name
   - Indonesian name
   - Stats (items, chapters, status)

### Test 2: Create New Subject
1. Go to admin: http://127.0.0.1:8000/admin/learning/subject/add/
2. Create a new subject with:
   - Name: テスト科目
   - Indonesian Name: Test Subject
   - Icon: school
   - Color: #e91e63
3. Save
4. Go back to http://127.0.0.1:8000/subjects/
5. **New subject should appear automatically** ✅

### Test 3: Delete "testing" Subject
1. Admin → Subjects → Delete "testing" (ID 7)
2. Refresh http://127.0.0.1:8000/subjects/
3. **"testing" should disappear** ✅

### Test 4: Search Functionality
1. Type in search box
2. Cards should filter correctly
3. "No results" message should appear when no matches

## Rollback Plan

If something goes wrong:

1. **Backup current template**:
   ```bash
   cd backend/templates/subjects
   cp subject_learning.html subject_learning.html.backup
   ```

2. **To restore**:
   ```bash
   cp subject_learning.html.backup subject_learning.html
   ```

## Expected Results After Implementation

✅ Subjects page loads from database
✅ New subjects appear automatically
✅ Deleted subjects disappear automatically
✅ Icons and colors come from admin settings
✅ Stats calculated dynamically
✅ Search/filter still works
✅ "学習開始" button works for all subjects

## Files to Modify

1. `backend/templates/subjects/subject_learning.html` (lines 390-603)
2. (Optional) `backend/apps/web/views.py` - `subject_learning_view` function

## Common Issues & Fixes

### Issue 1: Subjects not appearing
**Fix**: Check that subjects have `is_active=True`

### Issue 2: Icons not showing
**Fix**: Verify Material Icons CSS is loaded in `<head>`

### Issue 3: Colors look wrong
**Fix**: Check color format is `#RRGGBB` (6-digit hex with #)

### Issue 4: Chapter count is 0
**Fix**: Make sure Items and Chapters are created for the subject

### Issue 5: JavaScript errors on "学習開始" button
**Fix**: Make sure `startLearning()` function in `<script>` tag accepts subject names correctly

## Next Steps After Implementation

1. Test all functionality
2. Delete the "testing" subject (ID 7) if not needed
3. Create new subjects as needed - they'll appear automatically!
4. Customize icons/colors for each subject in admin
5. Remove any old static HTML files in `backend/static/subjects/` (if any)

## Related Files

- View: `backend/apps/web/views.py` - `subject_learning_view()`
- Template: `backend/templates/subjects/subject_learning.html`
- Model: `backend/apps/learning/models.py` - `Subject` class
- Admin: `backend/apps/learning/admin.py` - `SubjectAdmin` class

---

**Status**: 📝 Ready to implement
**Prerequisite**: ✅ Icon & Color fields added (completed)
**Estimated Time**: 10-15 minutes
**Difficulty**: Easy
