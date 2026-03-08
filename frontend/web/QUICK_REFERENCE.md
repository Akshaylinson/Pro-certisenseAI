# 🎨 CertiSense AI v3.0 - Quick UI Reference

## 🚀 Quick Start

### Access the Enhanced Dashboard
```
URL: http://localhost:5175
Login: Admin credentials
Theme: Professional White/Blue
Icons: FontAwesome 6.4.0
```

## 📦 New Components Available

### Layout Component
```jsx
<Layout
  title="Dashboard Title"
  subtitle="Optional Subtitle"
  userRole="Your Role"
  onLogout={handleLogout}
  navigationItems={[...]}
  activeModule={currentModule}
  onModuleChange={setModule}
  themeColor="blue"
>
  {children}
</Layout>
```

### StatCard
```jsx
<StatCard 
  title="Total Students"
  value={count}
  icon="fa-user-graduate"
  color="green"  // blue, green, purple, yellow, red, indigo
/>
```

### InfoCard
```jsx
<InfoCard title="Section Title">
  Content here
</InfoCard>
```

### Button
```jsx
<Button 
  variant="primary"    // primary, secondary, success, danger, warning
  size="md"           // sm, md, lg
  icon="fa-plus"
  onClick={handler}
>
  Button Text
</Button>
```

### Badge
```jsx
<Badge variant="success">  // success, danger, warning, info, neutral
  Status Text
</Badge>
```

## 🎨 Design Tokens

### Colors
```css
Primary Blue: #2563eb
Background: #f8fafc
White: #ffffff
Border: #e2e8f0
Text: #1e293b
```

### Spacing
```css
Section gap: 30px
Card padding: 20px
Component gap: 20px
Grid gap: 20px
```

### Typography
```css
Page Title: 24px bold
Section Title: 18px semibold
Body: 14px regular
Small: 12px
```

## 📋 Icon Mapping

| Module | Icon Class |
|--------|-----------|
| Dashboard | fa-chart-line |
| Institutes | fa-building-columns |
| Certificates | fa-certificate |
| Students | fa-user-graduate |
| Verifiers | fa-user-shield |
| Verifications | fa-check-double |
| Reports | fa-file-waveform |
| Feedback | fa-comments |
| Profile | fa-user |
| History | fa-clock-rotate-left |
| Verify | fa-magnifying-glass |
| Chatbot | fa-robot |

## 🔧 Common Patterns

### Table Pattern
```jsx
<InfoCard>
  <div className="table-container">
    <table>
      <thead>
        <tr>
          <th>Column 1</th>
          <th>Column 2</th>
        </tr>
      </thead>
      <tbody>
        {data.map(item => (
          <tr key={item.id}>
            <td>{item.value}</td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
</InfoCard>
```

### Form Pattern
```jsx
<InfoCard title="Form Title">
  <form className="space-y-4">
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label className="block font-medium mb-2">Label</label>
        <input type="text" className="w-full" required />
      </div>
    </div>
    <div className="flex gap-2">
      <Button type="submit" variant="success">Save</Button>
      <Button type="button" variant="secondary">Cancel</Button>
    </div>
  </form>
</InfoCard>
```

### Stats Grid Pattern
```jsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
  <StatCard title="Total" value={count} icon="fa-icon" color="blue" />
  <StatCard title="Active" value={count} icon="fa-icon" color="green" />
  <StatCard title="Pending" value={count} icon="fa-icon" color="yellow" />
  <StatCard title="Issues" value={count} icon="fa-icon" color="red" />
</div>
```

## ✅ Admin Dashboard Modules

### 1. Dashboard Analytics
- StatCards for metrics
- Verification rate display
- Certificate status breakdown
- Recent activity section

### 2. Manage Institutes
- Add institute form
- Scrollable table
- Status badges
- Delete actions

### 3. Manage Certificates
- Certificate list table
- Status indicators
- Empty state handling
- Verification counts

### 4. View Students
- Student roster table
- Institute linkage
- Certificate counts
- Read-only view

### 5. Manage Verifiers
- Add verifier form
- Verifier list table
- Type badges
- Status management

### 6. Monitor Verifications
- Verification history
- Result badges
- Confidence scores
- Flag suspicious items

### 7. Generate Reports
- Report cards with icons
- 4 report types
- AI features list
- One-click generation

### 8. Feedback Management
- Feedback table
- Priority badges
- Category tags
- Flag functionality

## 🎯 Testing Checklist

Quick test for each module:
- [ ] Navigation works
- [ ] Data loads correctly
- [ ] Tables scroll if needed
- [ ] Buttons respond to clicks
- [ ] Icons display properly
- [ ] Badges show correct colors
- [ ] Forms are aligned
- [ ] Mobile responsive

## 🐛 Troubleshooting

### Icons Not Showing
Check: index.html has FontAwesome CDN link

### Styles Not Applied
Check: Tailwind config file is correct

### Layout Broken
Check: Layout component is imported and used

### Tables Not Scrolling
Check: table-container class is applied

### Colors Wrong
Check: Using correct variant names

## 📱 Responsive Breakpoints

```css
Mobile: < 768px
  - Single column
  - Hamburger menu
  - Stacked buttons

Tablet: 768px - 1023px
  - Two columns
  - Collapsible sidebar
  - Compact layouts

Desktop: 1024px - 1919px
  - Three columns
  - Full sidebar
  - Standard spacing

Large: 1920px+
  - Four columns
  - Wide layouts
  - Maximum spacing
```

## 💨 Quick Tips

1. **Always use Layout component** for consistent structure
2. **Use StatCards** for statistics/metrics
3. **Wrap tables** in table-container div
4. **Use Badges** for all status indicators
5. **Use Buttons** with variants for actions
6. **Replace emojis** with FontAwesome icons
7. **Maintain spacing** - use 20px system
8. **Keep it responsive** - test on mobile

## 🎨 Color Coding Guide

**Blue** (#2563eb) - Primary actions, information
**Green** (#16a34a) - Success, active, valid
**Red** (#dc2626) - Danger, delete, invalid
**Yellow** (#eab308) - Warning, pending
**Purple** (#9333ea) - Special features
**Gray** (#64748b) - Secondary, neutral

---

**Last Updated**: March 8, 2026  
**Version**: 3.0 Enhanced  
**Status**: Production Ready ✅
