# Subject Icon & Color Setup Guide

## Overview

This guide explains how to customize icons and colors for subjects in the 科目学習 (Subject Learning) system. With this feature, you can control the appearance of each subject card directly from the Django admin interface.

## What Was Implemented

### 1. Database Changes
- Added `icon` field to Subject model (40 Material Icon choices)
- Added `color` field to Subject model (hex color codes)
- Migration applied: `0006_subject_color_subject_icon.py`

### 2. Admin Interface
- Icon and color fields now visible in Subject admin
- Dropdown selector with 40 icon choices (with emoji previews)
- Organized into fieldsets for better UX

### 3. Available Icons (40 choices)

#### Healthcare
- `medical_services` - 🏥 Medical Services
- `local_hospital` - 🏥 Hospital
- `health_and_safety` - 🩺 Health & Safety
- `elderly` - 👴 Elderly Care
- `psychology` - 🧠 Psychology

#### Communication
- `chat` - 💬 Chat
- `forum` - 💭 Forum
- `question_answer` - ❓ Q&A

#### People
- `people` - 👥 People
- `groups` - 👥 Groups
- `person` - 👤 Person

#### Education
- `assignment` - 📋 Assignment
- `task` - ✅ Task
- `quiz` - ❓ Quiz
- `school` - 🎓 School
- `menu_book` - 📖 Book (default)
- `auto_stories` - 📚 Stories
- `import_contacts` - 📕 Contacts

#### Places
- `home` - 🏠 Home
- `house` - 🏡 House
- `apartment` - 🏢 Apartment

#### Work & Business
- `work` - 💼 Work
- `business` - 💼 Business
- `science` - 🔬 Science
- `biotech` - 🧬 Biotech

#### Social
- `favorite` - ❤️ Favorite
- `star` - ⭐ Star
- `grade` - ⭐ Grade
- `volunteer_activism` - 🤝 Volunteer
- `handshake` - 🤝 Handshake
- `support` - 🆘 Support

#### Care & Services
- `child_care` - 👶 Child Care
- `face` - 😊 Face
- `restaurant` - 🍽️ Restaurant
- `fastfood` - 🍔 Food

#### Transportation
- `directions_car` - 🚗 Car
- `directions_bus` - 🚌 Bus
- `train` - 🚆 Train

#### Language
- `language` - 🌐 Language
- `translate` - 🔤 Translate

### 4. Suggested Color Codes

Use these hex codes for variety:
- **Green**: `#4caf50` (Healthcare, Medical)
- **Blue**: `#2196f3` (Communication, Learning)
- **Orange**: `#ff9800` (Social, People)
- **Purple**: `#9c27b0` (Work, Business)
- **Brown**: `#795548` (Culture, Lifestyle)
- **Red**: `#f44336` (Emergency, Important)
- **Teal**: `#009688` (Care, Support)
- **Indigo**: `#3f51b5` (Education, Training)
- **Pink**: `#e91e63` (Community, Social)
- **Amber**: `#ffc107` (Warning, Attention)

## How to Set Icons & Colors in Admin

### Step 1: Access Subject Admin
1. Navigate to: http://127.0.0.1:8000/admin/
2. Click on **"Subjects"** under the "Learning" section

### Step 2: Edit a Subject
1. Click on a subject name to edit it
2. You'll see three sections:
   - **Basic Information** (name, indonesian name, etc.)
   - **UI Customization** ← This is where you set icon/color
   - **Organization** (order, is_active)

### Step 3: Choose Icon
1. In the "UI Customization" section, find the **Icon** dropdown
2. Select an icon from the dropdown (you'll see emoji previews)
3. Example: For "介護試験対策", choose `medical_services` 🏥

### Step 4: Set Color
1. In the same section, find the **Color** field
2. Enter a hex color code (e.g., `#4caf50`)
3. Make sure to include the `#` symbol

### Step 5: Save
Click the **"Save"** button at the bottom

## Current Subjects & Recommended Settings

Based on your existing subjects (6 total):

### Subject 1: 介護試験対策 (Persiapan Ujian Kaigo)
**Recommended:**
- Icon: `medical_services` 🏥
- Color: `#4caf50` (green)
- Reason: Medical/healthcare focus

### Subject 2: 介護の実務会話 (Percakapan Praktis Kaigo)
**Recommended:**
- Icon: `chat` 💬
- Color: `#2196f3` (blue)
- Reason: Conversation/communication

### Subject 3: 日本人と会話 (Percakapan dengan Orang Jepang)
**Recommended:**
- Icon: `people` 👥
- Color: `#ff9800` (orange)
- Reason: Social interaction

### Subject 4: 特定技能評価試験 (Ujian Evaluasi Keterampilan Khusus)
**Recommended:**
- Icon: `assignment` 📋
- Color: `#9c27b0` (purple)
- Reason: Evaluation/assessment

### Subject 5: 日本の生活マナー (Etiket Kehidupan di Jepang)
**Recommended:**
- Icon: `home` 🏠
- Color: `#795548` (brown)
- Reason: Lifestyle/culture

### Subject 6: testing (testingID)
**Recommended:**
- Icon: `quiz` ❓
- Color: `#ffc107` (amber)
- Reason: Testing/development
- **Note**: Consider deleting this if it's just a test subject

## Automated Update Script (Optional)

If you want to update all subjects at once via script:

```python
# Run in Django shell: python manage.py shell

from apps.learning.models import Subject

# Subject 1: 介護試験対策
s1 = Subject.objects.get(id=1)
s1.icon = 'medical_services'
s1.color = '#4caf50'
s1.save()

# Subject 2: 介護の実務会話
s2 = Subject.objects.get(id=2)
s2.icon = 'chat'
s2.color = '#2196f3'
s2.save()

# Subject 3: 日本人と会話
s3 = Subject.objects.get(id=3)
s3.icon = 'people'
s3.color = '#ff9800'
s3.save()

# Subject 4: 特定技能評価試験
s4 = Subject.objects.get(id=4)
s4.icon = 'assignment'
s4.color = '#9c27b0'
s4.save()

# Subject 5: 日本の生活マナー
s5 = Subject.objects.get(id=5)
s5.icon = 'home'
s5.color = '#795548'
s5.save()

# Subject 6: testing
s6 = Subject.objects.get(id=7)
s6.icon = 'quiz'
s6.color = '#ffc107'
s6.save()

print("All subjects updated!")
```

## Next Step: Update Template

After setting icons and colors, the template needs to be updated to use these values dynamically. See `TEMPLATE_UPDATE_INSTRUCTIONS.md` for details.

## Verification

After setting icons/colors:
1. Go to Subjects list in admin
2. You should see the icon and color columns populated
3. Colors should display as hex codes (e.g., `#4caf50`)

## Troubleshooting

### Icons not appearing in dropdown
- Check that migration was applied: `python manage.py migrate learning`
- Restart the server if needed

### Colors not saving
- Make sure to include the `#` symbol
- Use 6-digit hex codes (e.g., `#4caf50`, not `#4cf`)

### Changes not visible on frontend
- Template update is required (Step A - see TEMPLATE_UPDATE_INSTRUCTIONS.md)
- The template is still hardcoded and needs to be made dynamic

## Files Modified

1. `backend/apps/learning/models.py` - Added icon/color fields
2. `backend/apps/learning/admin.py` - Updated admin interface
3. `backend/apps/learning/migrations/0006_subject_color_subject_icon.py` - Database migration

## Related Documentation

- Material Icons Reference: https://fonts.google.com/icons
- HTML Color Picker: https://htmlcolorcodes.com/
- Next: `TEMPLATE_UPDATE_INSTRUCTIONS.md` (to be created)

---

**Last Updated**: 2025-10-10
**Status**: ✅ Database & Admin Complete | ⏳ Template Update Pending
