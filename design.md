# 04 Frontend Specification Document — Hay Day Bot Suite

## 1. Design Philosophy
- **Realistic, Minimalist & Ultra-Premium**: Clean layout, generous white space, subtle borders, high contrast readability.
- **Strictly No Cheesy Neon or Overdone Cyberpunk**: Curated HSL dark palette with slate surfaces and natural emerald/gold farm accents.

## 2. Color Palette
- **Background Main**: `#0b0f17` (Deep Dark Slate)
- **Background Surface**: `#111827` (Card Background)
- **Background Card**: `#172033` (Elevated Tile)
- **Border Subtle**: `#26334d`
- **Primary Accent**: `#10b981` (Emerald Green)
- **Secondary Accent**: `#f59e0b` (Farm Gold)
- **Danger / Stop**: `#ef4444` (Crimson Red)
- **Text Primary**: `#f8fafc` (High Contrast White)
- **Text Secondary**: `#94a3b8` (Muted Slate)

## 3. Typography
- **Primary Body & Headings**: `Inter` (Google Fonts, weights: 400, 500, 600, 700)
- **Terminal & Logs**: `JetBrains Mono` (Google Fonts, weights: 400, 500)

## 4. Component Styles & Layout
- **Sticky Header**: 16px vertical padding, backdrop blur, logo, status chips with animated pulsing dots.
- **Top Metrics Grid**: Responsive 4-card grid displaying Target Crop, Shop Crates, AI Engines, and Anti-Detection status.
- **Dashboard Split**: Two-column layout (50/50 desktop, 1-column mobile) balancing 13 Subsystems modules on the left with Live Console logs on the right.
- **Micro-Interactions**: Smooth 0.2s hover transforms, glowing borders on action buttons, and automatic scrolling log feed.
