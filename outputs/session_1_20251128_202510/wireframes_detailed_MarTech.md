# Feature Screen

```
┌──────────────────────────────────────────────────────────────────┐
│ [App Logo]        [Main Navigation]                               [User Profile] │
└──────────────────────────────────────────────────────────────────┘
│                                                                                  │
│ ┌──────────────────────────────────────────────────────────────────────────────┐ │
│ │ Breadcrumbs: Home > Blog Posts > New Blog Post                 [← Back to Drafts] │
│ └──────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                  │
│ ┌──────────────────────────────────────────────────────────────────────────────┐ │
│ │                                                                              │ │
│ │ Screen: New Blog Post | Purpose: Generate, edit, and publish blog content.     │
│ │ User Context: Arrived from "My Blog Drafts" list or main "Blog Posts" menu.    │
│ │ Priority: AI Generation > Editing > WordPress Publishing                       │
│ │                                                                              │ │
│ └──────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                  │
│ ┌───────────────────────────────┬──────────────────────────────────────────────┐ │
│ │                             │                                              │ │
│ │ Zone: Content Creation      │ Zone: Publishing & Actions                   │ │
│ │ Content: AI input, Editor   │ Content: WordPress controls, Save/Publish    │ │
│ │ Size: ~70% width            │ Size: ~30% width                             │ │
│ │ Position: Left              │ Position: Right                              │ │
│ │                             │                                              │ │
│ ├───────────────────────────────┼──────────────────────────────────────────────┤ │
│ │                             │                                              │ │
│ │ Element: Section Heading    │ Element: Section Heading                     │ │
│ │ Type: H2                    │ Type: H3                                     │ │
│ │ Purpose: Guide user         │ Purpose: Organize publishing controls        │ │
│ │ Priority: 2                 │ Priority: 3                                  │ │
│ │                             │                                              │ │
│ │ ┌──────────────────────────┐│ ┌──────────────────────────────────────────┐ │
│ │ │ 1. Generate Blog Post    ││ │ 3. WordPress Publishing Options          │ │
│ │ └──────────────────────────┘│ └──────────────────────────────────────────┘ │
│ │                             │                                              │ │
│ │ Element: Topic Input Label  │ Element: WP Site Selector                    │ │
│ │ Type: Label                 │ Type: Dropdown / Button                      │ │
│ │ Purpose: Instruct user      │ Purpose: Choose target WP site               │ │
│ │ Priority: 2                 │ Priority: 3                                  │ │
│ │                             │                                              │ │
│ │ Topic or Keywords           │ Select WordPress Site:                       │ │
│ │ ┌──────────────────────────┐│ ┌──────────────────────────────────────────┐ │
│ │ │ [Text input for topic]   ││ │ ▼ My WordPress Site 1 (Connected)        │ │
│ │ └──────────────────────────┘│ ├──────────────────────────────────────────┤ │
│ │                             │ │ + Connect New WordPress Site             │ │
│ │ Element: Generate Button    │ └──────────────────────────────────────────┘ │
│ │ Type: Primary Button        │                                              │ │
│ │ Purpose: Trigger AI         │ Element: Category Selector                   │ │
│ │ Priority: 1                 │ Type: Dropdown                               │ │
│ │                             │ Purpose: Assign WP category                  │ │
│ │ ┌──────────────────────────┐│ Priority: 4                                  │ │
│ │ │ [ Generate Draft ]       ││                                              │ │
│ │ └──────────────────────────┘│ Select Category:                             │ │
│ │                             │ ┌──────────────────────────────────────────┐ │
│ │                             │ │ ▼ (e.g., Marketing, News)                │ │
│ │ Element: Loading Indicator  │ └──────────────────────────────────────────┘ │
│ │ Type: Spinner / Text        │                                              │ │
│ │ Purpose: Feedback for AI    │ Element: Tags Input                          │ │
│ │ Priority: 5                 │ Type: Text Input with suggestions            │ │
│ │                             │ Purpose: Add WP tags                         │ │
│ │ (Loading AI draft...)       │                                              │ │
│ │                             │ Tags:                                        │ │
│ │ ┌──────────────────────────┐│ ┌──────────────────────────────────────────┐ │
│ │ │ 2. Review & Edit Content ││ │ [Text input for tags, e.g., AI, Blog ]   │ │
│ │ └──────────────────────────┘│ └──────────────────────────────────────────┘ │
│ │                             │                                              │ │
│ │ Element: Post Title Input   │ Element: Status Selector                     │ │
│ │ Type: Text Input            │ Type: Dropdown                               │ │
│ │ Purpose: Main title         │ Purpose: Set WP post status                  │ │
│ │ Priority: 2                 │ Priority: 4                                  │ │
│ │                             │                                              │ │
│ │ Post Title                  │ Publishing Status:                           │ │
│ │ ┌──────────────────────────┐│ ┌──────────────────────────────────────────┐ │
│ │ │ [AI Generated Title]     ││ │ ▼ Publish (or Draft, Pending Review)     │ │
│ │ └──────────────────────────┘│ └──────────────────────────────────────────┘ │
│ │                             │                                              │ │
│ │ Element: Rich Text Editor   │ ┌──────────────────────────────────────────┐ │
│ │ Type: WYSIWYG Editor        │ │                                          │ │
│ │ Purpose: Edit blog content  │ │ Element: Save Draft Button               │ │
│ │ Priority: 1                 │ │ Type: Secondary Button                   │ │
│ │                             │ │ Purpose: Persist changes                 │ │
│ │ ┌──────────────────────────┐│ │ Priority: 2                              │ │
│ │ │ [B I U H1 H2 Link Img]   ││ │                                          │ │
│ │ ├──────────────────────────┤│ │ [ Save Draft ]                           │ │
│ │ │                          ││ │                                          │ │
│ │ │ [AI Generated Blog Body] ││ │ Element: Publish Button                  │ │
│ │ │                          ││ │ Type: Primary Button                     │ │
│ │ │                          ││ │ Purpose: Initiate WP publishing          │ │
│ │ │                          ││ │ Priority: 1                              │ │
│ │ │                          ││ │                                          │ │
│ │ │                          ││ │ [ Publish to WordPress ]                 │ │
│ │ │                          ││ │                                          │ │
│ │ └──────────────────────────┘│ └──────────────────────────────────────────┘ │
│ │                             │                                              │ │
│ └───────────────────────────────┴──────────────────────────────────────────────┘ │
│                                                                                  │
│ ┌──────────────────────────────────────────────────────────────────────────────┐ │
│ │ [Footer with copyright and links]                                            │ │
│ └──────────────────────────────────────────────────────────────────────────────┘ │
```

---

### Wireframe Specification: "New Blog Post" Screen

This wireframe details the "New Blog Post" screen, allowing users to generate AI content, edit it, and publish directly to WordPress.

### 1. Screen Analysis

*   **Screen: New Blog Post**
    *   **Purpose:** To provide an end-to-end workflow for generating AI-powered blog content, editing it, and publishing it to a connected WordPress website.
    *   **User Goals:**
        *   Generate a blog post draft quickly using AI based on a topic.
        *   Refine and customize the generated content using a rich text editor.
        *   Securely save the content as a draft within the application.
        *   Connect to WordPress sites and configure publishing options.
        *   Publish the final blog post to WordPress.
    *   **User Context:** Users typically arrive from the "My Blog Drafts" list (by clicking a "New Blog Post" button) or directly from the main application navigation's "Blog Posts" menu item. After using this screen, they will either return to "My Blog Drafts" (after saving or publishing) or navigate to their live WordPress site (after publishing).
    *   **Content Priority:** The highest priority is the AI topic input and generation, followed by the rich text editor for content refinement. WordPress publishing options and final actions ("Save Draft", "Publish") are also critical.

### 2. UI Elements Identification

1.  **Element: App Header**
    *   **Type:** Global Header
    *   **Purpose:** Branding, main navigation, user account access.
    *   **Priority:** 5 (Always visible)
2.  **Element: Breadcrumbs / Back Link**
    *   **Type:** Text Link / Button
    *   **Purpose:** Indicate current location, allow navigation back to "My Blog Drafts".
    *   **Priority:** 4
3.  **Element: "1. Generate Blog Post" Section Heading**
    *   **Type:** H2 Heading
    *   **Purpose:** Guide the user to the initial step.
    *   **Priority:** 2
4.  **Element: Topic or Keywords Input**
    *   **Type:** Text Input (single line)
    *   **Purpose:** User enters the desired topic for AI generation.
    *   **Priority:** 1
    *   **Accessibility:** `aria-label="Topic or Keywords for blog post generation"`
5.  **Element: Generate Draft Button**
    *   **Type:** Primary Button
    *   **Purpose:** Initiates the AI content generation process.
    *   **Priority:** 1
    *   **Accessibility:** `aria-label="Generate Blog Post Draft"`
6.  **Element: AI Generation Loading Indicator**
    *   **Type:** Spinner / Text message
    *   **Purpose:** Provide feedback during AI processing (async operation).
    *   **Priority:** 5 (Conditional)
    *   **Accessibility:** `aria-live="polite"` with "Generating draft, please wait..."
7.  **Element: "2. Review & Edit Content" Section Heading**
    *   **Type:** H2 Heading
    *   **Purpose:** Guide the user to edit the generated content.
    *   **Priority:** 2
8.  **Element: Post Title Input**
    *   **Type:** Text Input
    *   **Purpose:** Allows user to edit the blog post's main title (pre-filled by AI).
    *   **Priority:** 2
    *   **Accessibility:** `aria-label="Blog Post Title"`
9.  **Element: Rich Text Editor Toolbar**
    *   **Type:** Toolbar with buttons
    *   **Purpose:** Provide formatting options (Bold, Italic, Underline, Headings, Link, Image).
    *   **Priority:** 2
    *   **Accessibility:** Ensure all toolbar buttons are keyboard accessible and have descriptive `aria-label`s.
10. **Element: Rich Text Editor Area**
    *   **Type:** WYSIWYG Text Area
    *   **Purpose:** Displays the AI-generated content for extensive editing and refinement.
    *   **Priority:** 1 (Core content area)
    *   **Accessibility:** `role="textbox"` with `aria-multiline="true"`, `aria-label="Blog Post Content Editor"`
11. **Element: "3. WordPress Publishing Options" Section Heading**
    *   **Type:** H3 Heading
    *   **Purpose:** Organizes controls for WordPress integration.
    *   **Priority:** 3
12. **Element: Select WordPress Site Dropdown**
    *   **Type:** Dropdown Selector
    *   **Purpose:** User chooses which connected WordPress site to publish to.
    *   **Priority:** 3
    *   **Accessibility:** `aria-label="Select WordPress Site"`
13. **Element: "Connect New WordPress Site" Button/Link**
    *   **Type:** Secondary Button / Link
    *   **Purpose:** Initiates the workflow to add a new WordPress connection (opens a modal/new screen).
    *   **Priority:** 4
    *   **Accessibility:** `aria-label="Connect a New WordPress Site"`
14. **Element: Select Category Dropdown**
    *   **Type:** Dropdown Selector (populated from selected WP site)
    *   **Purpose:** Assigns the blog post to an existing WordPress category.
    *   **Priority:** 4
    *   **Accessibility:** `aria-label="Select Blog Post Category"`
15. **Element: Tags Input**
    *   **Type:** Text Input with auto-suggest/autocomplete
    *   **Purpose:** Allows users to add relevant tags to the WordPress post.
    *   **Priority:** 4
    *   **Accessibility:** `aria-label="Add Blog Post Tags"`
16. **Element: Publishing Status Dropdown**
    *   **Type:** Dropdown Selector (options: Draft, Pending Review, Publish)
    *   **Purpose:** Sets the status of the post on WordPress upon publication.
    *   **Priority:** 4
    *   **Accessibility:** `aria-label="Select Publishing Status"`
17. **Element: Save Draft Button**
    *   **Type:** Secondary Button
    *   **Purpose:** Saves the current state of the blog post within the application.
    *   **Priority:** 2 (for actions)
    *   **Accessibility:** `aria-label="Save Blog Post Draft"`
18. **Element: Publish to WordPress Button**
    *   **Type:** Primary Button
    *   **Purpose:** Triggers the process of publishing the content to the selected WordPress site.
    *   **Priority:** 1 (for actions)
    *   **Accessibility:** `aria-label="Publish Blog Post to WordPress"`
19. **Element: Global Footer**
    *   **Type:** Footer
    *   **Purpose:** Legal information, secondary links.
    *   **Priority:** 5 (Always visible)

### 3. Layout Structure

*   **Grid System:** Assumed a 12-column grid for desktop.
*   **Content Zones:**
    *   **Header (Full Width):** Standard app header for branding and global navigation.
    *   **Breadcrumbs/Context (Full Width):** Above main content, for navigation and context.
    *   **Main Content Area (70% Width - Left):**
        *   **AI Input Section:** At the top, a clear area for topic input and the "Generate Draft" button.
        *   **Rich Text Editor Section:** Below AI input, occupying the largest visual space, featuring the title input and the WYSIWYG editor.
    *   **Publishing & Actions Sidebar (30% Width - Right):**
        *   **WordPress Options:** Grouped fields for selecting a WordPress site, categories, tags, and publishing status.
        *   **Action Buttons:** "Save Draft" and "Publish to WordPress" buttons, visually prominent.
    *   **Footer (Full Width):** Standard app footer.
*   **Visual Hierarchy:** The AI input field and "Generate Draft" button are immediately visible. After generation, the Rich Text Editor dominates the left panel, inviting editing. The WordPress publishing options on the right are clearly secondary for configuration, with the "Publish" button as the ultimate call to action.
*   **Spacing:** Generous padding around sections and elements to reduce cognitive load and improve readability. Consistent spacing between input fields and buttons.
*   **Responsive Behavior:**
    *   **Mobile:** The two main content zones (Content Creation and Publishing & Actions) will stack vertically. The left main content area will take full width, followed by the right publishing sidebar now rendered full width below the editor.
    *   **Editor:** The rich text editor will fluidly adjust its width.
    *   **Navigation:** Main navigation might collapse into a hamburger menu.

### 4. Navigation Flow

*   **Entry Points:**
    *   **From "My Blog Drafts":** User clicks a "New Blog Post" button on the drafts list screen.
    *   **From Main Navigation:** User selects "Blog Posts" from the main menu, then clicks an implicit "New Blog Post" action (or is redirected if no drafts exist).
*   **Exit Points:**
    *   **"Back to Drafts" Link:** Returns to the "My Blog Drafts" list without saving unsaved changes (with a confirmation prompt).
    *   **"Save Draft" Button:** Stays on the current "New Blog Post" screen, showing a success message, and ensuring the draft is saved to "My Blog Drafts".
    *   **"Publish to WordPress" Button:** Stays on the current "New Blog Post" screen, showing a success message and a link to the live post, and changes the internal status of the draft.
    *   **"Connect New WordPress Site" Action:** Opens a modal or navigates to a separate "Connect WordPress Site" screen, returning to this screen upon completion.
*   **Navigation Aids:** Breadcrumbs clearly show the user's path. A prominent "Back to My Blog Drafts" link is available.
*   **Deep Links:** Not primarily applicable for a creation screen, but published posts could link back to their editable version.

### 5. User Interactions

*   **Topic Input:**
    *   **Action:** User types text.
    *   **Feedback:** Text appears in the input field.
    *   **State:** Default, Focused, Empty (validation).
*   **Generate Draft Button:**
    *   **Action:** User clicks.
    *   **Feedback:** Button enters a loading state (e.g., disabled, spinner appears).
    *   **State:** Default, Hover, Active, Loading, Disabled (if input is empty).
*   **AI Generation:**
    *   **Action:** System generating.
    *   **Feedback:** Loading spinner and "Generating AI draft..." message displayed prominently in the content area.
    *   **State:** Loading.
    *   **Success:** AI-generated content populates the title and editor, loading indicator disappears.
    *   **Error:** Error message ("Failed to generate...") displayed if AI service fails.
*   **Rich Text Editor (Toolbar Buttons):**
    *   **Action:** User clicks a formatting button (e.g., Bold).
    *   **Feedback:** Text in editor changes format; button highlights (active state).
    *   **State:** Default, Hover, Active.
*   **Rich Text Editor (Content Area):**
    *   **Action:** User types, selects text.
    *   **Feedback:** Text appears, selection highlights.
    *   **State:** Default, Focused.
*   **Save Draft Button:**
    *   **Action:** User clicks.
    *   **Feedback:** Button enters loading state briefly. Success toast/message ("Draft saved!") appears.
    *   **State:** Default, Hover, Active, Loading.
*   **WordPress Dropdowns (Site, Category, Status):**
    *   **Action:** User clicks to open dropdown, selects an option.
    *   **Feedback:** Dropdown opens, selection highlights, dropdown closes.
    *   **State:** Default, Open, Selected.
*   **Tags Input:**
    *   **Action:** User types, system offers suggestions (if applicable).
    *   **Feedback:** Text appears, suggestions display below input.
    *   **State:** Default, Focused, With Suggestions.
*   **Publish to WordPress Button:**
    *   **Action:** User clicks.
    *   **Feedback:** Button enters loading state briefly. Success toast/message ("Blog published!") appears with a link to the live post.
    *   **State:** Default, Hover, Active, Loading, Disabled (if no WP site selected or other errors).
    *   **Error:** Error toast/message ("Failed to publish...") if WordPress API fails.

### 6. Accessibility Considerations

*   **Keyboard Navigation:**
    *   Tab order will logically follow the visual flow: App Header -> Breadcrumbs/Back Link -> Topic Input -> Generate Button -> Post Title Input -> Rich Text Editor Toolbar (left-to-right, then top-to-bottom) -> Rich Text Editor Content -> WordPress Site Selector -> Connect New WP Site -> Category Selector -> Tags Input -> Status Selector -> Save Draft Button -> Publish Button -> Footer.
    *   All interactive elements (buttons, inputs, links, dropdowns) must be reachable and operable via keyboard.
*   **Screen Reader Support:**
    *   All headings (H1/H2/H3) used semantically.
    *   Labels are clearly associated with their input fields using `<label for="...">`.
    *   `aria-label` or `aria-labelledby` attributes for complex components like the rich text editor and dropdowns for clarity.
    *   `aria-live="polite"` for loading indicators and success/error messages to announce changes to screen readers.
    *   Images/Icons in the rich text editor toolbar will have descriptive `alt` text or `aria-label`s.
*   **Color Contrast:**
    *   All text against its background must meet WCAG 2.1 AA contrast ratios (minimum 4.5:1 for regular text, 3:1 for large text).
    *   Interactive elements (buttons, links) will also have sufficient contrast in their default, hover, and active states.
*   **Focus Indicators:**
    *   Clear, visible focus outlines will be provided for all interactive elements when navigated via keyboard. This can be a distinct border, highlight, or shadow.
*   **Alt Text:**
    *   Any functional icons (e.g., those in the rich text editor toolbar) will have appropriate `alt` attributes or `aria-label`s.
    *   Users inserting images will be prompted to provide alt text for accessibility.
*   **Error Handling:** Error messages will be clear, concise, and programmatically associated with the input field they relate to, allowing screen readers to announce them effectively.

## UI Elements

- User Profile
- Input Field
- Dropdown
- Image
- Text Area

# Settings

```
┌──────────────────────────────────────────────────────────────────┐
│ [App Logo]        [Main Navigation]                               [User Profile] │
└──────────────────────────────────────────────────────────────────┘
│                                                                                  │
│ ┌──────────────────────────────────────────────────────────────────────────────┐ │
│ │ Breadcrumbs: Home > Settings                                                 │ │
│ └──────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                  │
│ ┌───────────────────────────────────┬──────────────────────────────────────────┐ │
│ │                                   │                                          │ │
│ │ Zone: Settings Navigation         │ Zone: Settings Content (Dynamic)         │ │
│ │ Content: List of setting categories │ Content: Details for selected category │ │
│ │ Size: ~25% width                  │ Size: ~75% width                         │ │
│ │ Position: Left                    │ Position: Right                          │ │
│ │                                   │                                          │ │
│ ├───────────────────────────────────┼──────────────────────────────────────────┤ │
│ │                                   │                                          │ │
│ │ Element: Section Heading          │ Element: Active Settings Section Title   │ │
│ │ Type: H2                          │ Type: H1 (dynamic)                       │ │
│ │ Purpose: Organize settings categories │ Purpose: Clearly state active settings section │
│ │ Priority: 4                       │ Priority: 1                              │ │
│ │                                   │                                          │ │
│ │ ┌───────────────────────────────┐ │ ┌──────────────────────────────────────────┐ │
│ │ │ Settings                      │ │ │ WordPress Connections                    │
│ │ ├───────────────────────────────┤ │ └──────────────────────────────────────────┘ │
│ │ │                               │ │                                              │ │
│ │ │ Element: Nav Item (Profile)   │ │ Element: Sub-section Heading             │ │
│ │ │ Type: Link / Button           │ │ Type: H2                                 │ │
│ │ │ Purpose: Navigate to profile  │ │ Purpose: Introduce connected sites list  │ │
│ │ │ Priority: 1                   │ │ Priority: 2                              │ │
│ │ │                               │ │                                              │ │
│ │ │ [ Profile ]                   │ │ ┌──────────────────────────────────────────┐ │
│ │ │                               │ │ │ Connected WordPress Sites                │ │
│ │ │ Element: Nav Item (Security)  │ │ └──────────────────────────────────────────┘ │
│ │ │ Type: Link / Button           │ │                                              │ │
│ │ │ Purpose: Navigate to security │ │ Element: Table/List of WP sites          │ │
│ │ │ Priority: 2                   │ │ Type: Data Table / Card List             │ │
│ │ │                               │ │ Purpose: Display/manage connections      │ │
│ │ │ [ Security ]                  │ │ Priority: 1                              │ │
│ │ │                               │ │                                              │ │
│ │ │ Element: Nav Item (Billing)   │ │ ┌──────────────────────────────────────────┐ │
│ │ │ Type: Link / Button           │ │ │ Site URL                  Status Actions │ │
│ │ │ Purpose: Navigate to billing  │ │ ├──────────────────────────────────────────┤ │
│ │ │ Priority: 3                   │ │ │ example.com/blog/       Connected [Edit] [Disconnect] │
│ │ │                               │ │ ├──────────────────────────────────────────┤ │
│ │ │ [ Billing & Plans ]           │ │ │ clientmarketing.net     Connected [Edit] [Disconnect] │
│ │ │                               │ │ ├──────────────────────────────────────────┤ │
│ │ │ Element: Nav Item (WP Connect)│ │ │ (No Sites Connected Message / More sites...) │
│ │ │ Type: Link / Button           │ │ └──────────────────────────────────────────┘ │
│ │ │ Purpose: Manage WP sites      │ │                                              │ │
│ │ │ Priority: 1 (for new feature) │ │ Element: Add WP Site Button              │ │
│ │ │                               │ │ Type: Primary Button                     │ │
│ │ │ [ WordPress Connections ]     │ │ Purpose: Initiate new WP connection      │ │
│ │ │                               │ │ Priority: 2                              │ │
│ │ │ Element: Nav Item (AI Settings) │ │                                              │ │
│ │ │ Type: Link / Button           │ │ ┌──────────────────────────────────────────┐ │
│ │ │ Purpose: Configure AI         │ │ │ [ + Connect New WordPress Site ]         │ │
│ │ │ Priority: 2 (for new feature) │ │ └──────────────────────────────────────────┘ │
│ │ │                               │ │                                              │ │
│ │ │ [ AI Generation Settings ]    │ │ ┌──────────────────────────────────────────┐ │
│ │ │                               │ │ │ AI Generation Settings                   │ │
│ │ │ Element: Nav Item (Integrations)│ │ └──────────────────────────────────────────┘ │
│ │ │ Type: Link / Button           │ │                                              │ │
│ │ │ Purpose: Manage other integrations │ │ Element: Tone Label + Dropdown           │ │
│ │ │ Priority: 4                   │ │ Type: Label & Dropdown                   │ │
│ │ │                               │ │ Purpose: Set default AI tone             │ │
│ │ │ [ Other Integrations ]        │ │ Priority: 3                              │ │
│ │ │                               │ │                                              │ │
│ │ └───────────────────────────────┘ │ Default Tone:                              │ │
│ │                                   │ ┌──────────────────────────────────────────┐ │
│ │                                   │ │ ▼ Professional                           │ │
│ │                                   │ └──────────────────────────────────────────┘ │
│ │                                   │                                              │ │
│ │                                   │ Element: Length Label + Dropdown/Slider  │ │
│ │                                   │ Type: Label & Dropdown/Slider            │ │
│ │                                   │ Purpose: Set default AI length           │ │
│ │                                   │ Priority: 3                              │ │
│ │                                   │                                              │ │
│ │                                   │ Default Length:                            │ │
│ │                                   │ ┌──────────────────────────────────────────┐ │
│ │                                   │ │ ▼ 500-750 words                          │ │
│ │                                   │ └──────────────────────────────────────────┘ │
│ │                                   │                                              │ │
│ │                                   │ Element: Save AI Settings Button         │ │
│ │                                   │ Type: Primary Button                     │ │
│ │                                   │ Purpose: Persist AI settings             │ │
│ │                                   │ Priority: 1 (for this section)           │ │
│ │                                   │                                              │ │
│ │                                   │ ┌──────────────────────────────────────────┐ │
│ │                                   │ │ [ Save AI Settings ]                     │ │
│ │                                   │ └──────────────────────────────────────────┘ │
│ │                                   │                                              │ │
│ └───────────────────────────────────┴──────────────────────────────────────────┘ │
│                                                                                  │
│ ┌──────────────────────────────────────────────────────────────────────────────┐ │
│ │ [Footer with copyright and links]                                            │ │
│ └──────────────────────────────────────────────────────────────────────────────┘ │
```

---

### Wireframe Specification: "Settings" Screen

This wireframe outlines a comprehensive "Settings" screen within the social marketing application, designed to manage user-specific preferences and integrations, prominently featuring new sections for WordPress connections and AI generation settings.

### 1. Screen Analysis

*   **Screen: Settings**
    *   **Purpose:** To serve as a central hub for users to view and modify all application-wide configurations, personal account details, security, billing, and the new AI Blog Generator and WordPress Publisher feature settings.
    *   **User Goals:**
        *   Update personal profile information (name, email).
        *   Manage security settings (password change, 2FA).
        *   Review subscription details and manage payment methods.
        *   Connect new WordPress websites.
        *   View, edit, or disconnect existing WordPress site connections.
        *   Configure default AI generation parameters (e.g., content tone, desired length).
        *   Manage other third-party integrations.
    *   **User Context:** Users typically navigate to the Settings screen from the global application header (e.g., clicking their user profile icon or a "Settings" link). Their intent could range from a routine check of their profile to an urgent need to update billing or configure a new WordPress integration. They will primarily exit by selecting another main navigation item or using the browser's back functionality.
    *   **Content Priority:**
        *   **High:** User Profile, Security, WordPress Connections (adding, managing, disconnecting).
        *   **Medium:** Billing & Plans, AI Generation Settings (setting defaults).
        *   **Low:** Other Integrations (as generic placeholder).

### 2. UI Elements Identification

1.  **Element: App Header**
    *   **Type:** Global Header
    *   **Purpose:** Application branding, primary navigation access, and user profile shortcuts.
    *   **Priority:** 5
2.  **Element: Breadcrumbs**
    *   **Type:** Text Link (e.g., "Home > Settings")
    *   **Purpose:** Provides contextual navigation and indicates the user's current location within the application hierarchy.
    *   **Priority:** 4
3.  **Element: Settings Navigation (Sidebar)**
    *   **Type:** Vertical Navigation List
    *   **Purpose:** Allows users to efficiently switch between different categories of settings without reloading the entire page.
    *   **Priority:** 1 (Navigational)
4.  **Element: Nav Item (Profile, Security, Billing & Plans, WordPress Connections, AI Generation Settings, Other Integrations)**
    *   **Type:** Link / Button (within Settings Navigation Sidebar)
    *   **Purpose:** Each item serves as an entry point to a specific settings category.
    *   **Priority (relative to feature):** WordPress Connections (1), AI Generation Settings (2), Profile (1), Security (2), Billing & Plans (3), Other Integrations (4).
    *   **Accessibility:** Each link will have a clear, descriptive accessible name (`aria-label`) and `aria-current="page"` when active.
5.  **Element: Active Settings Section Title**
    *   **Type:** H1 Heading (Dynamic)
    *   **Purpose:** Clearly states the name of the currently active settings category, reinforcing user context.
    *   **Priority:** 1
6.  **Element: Sub-section Heading (e.g., "Connected WordPress Sites")**
    *   **Type:** H2 Heading
    *   **Purpose:** Organizes content within a larger settings category, breaking it into manageable sub-sections.
    *   **Priority:** 2
7.  **Element: Table/List of WP Sites**
    *   **Type:** Data Table or Card List
    *   **Purpose:** Displays a tabular or card-based view of all WordPress sites currently connected to the application, including their status.
    *   **Priority:** 1 (Core content of the WordPress Connections section)
    *   **Columns (if table):** Site URL, Connection Status, Actions (Edit, Disconnect).
    *   **Accessibility:** Table headers will use `<th>` with `scope` attributes. Action buttons will have descriptive `aria-label`s.
8.  **Element: Edit Button (for each WP site)**
    *   **Type:** Secondary Button / Icon Button
    *   **Purpose:** Allows users to modify details (e.g., refresh credentials) or settings for a specific connected WordPress site.
    *   **Priority:** 3
    *   **Accessibility:** `aria-label="Edit connection for [Site URL]"`
9.  **Element: Disconnect Button (for each WP site)**
    *   **Type:** Destructive Button / Icon Button
    *   **Purpose:** Allows users to securely remove a connected WordPress site. This action will typically require a confirmation step.
    *   **Priority:** 3
    *   **Accessibility:** `aria-label="Disconnect [Site URL]"`
10. **Element: "+ Connect New WordPress Site" Button**
    *   **Type:** Primary Button
    *   **Purpose:** Initiates the workflow for adding a new WordPress site connection to the application.
    *   **Priority:** 2
    *   **Accessibility:** `aria-label="Connect a New WordPress Site"`
11. **Element: Sub-section Heading (e.g., "AI Generation Settings")**
    *   **Type:** H2 Heading
    *   **Purpose:** Title for the default AI content generation settings.
    *   **Priority:** 2
12. **Element: Default Tone Label + Dropdown**
    *   **Type:** Label & Dropdown Selector
    *   **Purpose:** Allows users to set a preferred default tone for all AI-generated blog posts.
    *   **Priority:** 3
    *   **Accessibility:** Label is linked to the dropdown; dropdown has `aria-label="Default AI Generation Tone"`.
13. **Element: Default Length Label + Dropdown/Slider**
    *   **Type:** Label & Dropdown Selector or Slider
    *   **Purpose:** Allows users to set a preferred default length range for AI-generated blog posts.
    *   **Priority:** 3
    *   **Accessibility:** Label is linked to the control; control has `aria-label="Default AI Generation Length"`.
14. **Element: Save AI Settings Button**
    *   **Type:** Primary Button
    *   **Purpose:** Saves the configured default AI generation settings.
    *   **Priority:** 1 (for this specific settings section)
    *   **Accessibility:** `aria-label="Save AI Generation Settings"`
15. **Element: Global Footer**
    *   **Type:** Footer
    *   **Purpose:** Contains copyright information and secondary legal or help links.
    *   **Priority:** 5

### 3. Layout Structure

*   **Grid System:** Assumes a 12-column responsive grid for desktop, adapting to smaller breakpoints.
*   **Content Zones:**
    *   **Header (Full Width):** Consistent global header.
    *   **Breadcrumbs (Full Width):** Placed directly below the header for navigational context.
    *   **Settings Navigation Sidebar (Desktop: ~25% Width):**
        *   Positioned on the left, containing a list of `Nav Item` links.
        *   This area is visually distinct, acting as the primary navigation for settings categories.
        *   It should remain fixed or sticky on scroll for desktop to allow easy switching between sections.
    *   **Settings Content Area (Desktop: ~75% Width):**
        *   Positioned on the right, dynamically displaying content based on the selected `Nav Item`.
        *   Each content section begins with an `Active Settings Section Title` (H1), followed by relevant `Sub-section Heading` (H2s) and associated UI elements (tables, forms, buttons).
        *   Content within sections (e.g., the WordPress sites list or AI settings form) will utilize vertical stacking and appropriate spacing.
    *   **Footer (Full Width):** Consistent global footer.
*   **Visual Hierarchy:** The two-column layout immediately establishes the primary navigation (left) and the detailed content (right). The `Active Settings Section Title` and `Sub-section Headings` guide the user through the specific content. Primary action buttons (`+ Connect New WordPress Site`, `Save AI Settings`) are designed for prominence within their respective sections.
*   **Spacing:** Generous padding around major content zones and internal spacing between elements (e.g., form fields, buttons) to improve readability and reduce visual clutter. Vertical spacing ensures clear separation between sub-sections.
*   **Responsive Behavior:**
    *   **Mobile (Small Screens):** The `Settings Navigation` sidebar will transform. It could become a full-width dropdown selector at the top of the screen (e.g., "Settings: [Dropdown of categories]") or a slide-in overlay menu. The `Settings Content Area` will expand to full width, with sections and elements stacking vertically.
    *   **Tables:** The `Table/List of WP Sites` will likely convert from a traditional table to a card-based layout, where each card represents a WordPress site and contains its details and action buttons.
    *   **Form Fields:** Input fields and dropdowns will occupy full width or adjust proportionally.

### 4. Navigation Flow

*   **Entry Points:**
    *   **Global Header:** Clicking the user profile icon or a dedicated "Settings" link.
    *   **Direct Link:** Potentially via a deep link from another part of the application or an email.
*   **Exit Points:**
    *   **Main Navigation:** Clicking any primary navigation item (e.g., "Dashboard," "Campaigns") in the global header.
    *   **Browser Back Button:** Returns to the previously viewed screen.
    *   **Within Settings:** Clicking a different `Nav Item` in the sidebar essentially 'exits' the current section's content and 'enters' a new one.
*   **Navigation Aids:**
    *   **Breadcrumbs:** "Home > Settings" provides context.
    *   **Settings Navigation Sidebar:** The primary means of navigating between different categories of settings, with the active item clearly highlighted.
*   **Deep Links:** Specific settings categories (e.g., `/settings/wordpress` or `/settings/ai-generation`) could be directly accessible via deep links.

### 5. User Interactions

*   **Settings Navigation Item Click:**
    *   **Action:** User clicks a `Nav Item` (e.g., "WordPress Connections").
    *   **Feedback:** The clicked item visually highlights, and the `Settings Content Area` dynamically updates to display the corresponding content. The `Active Settings Section Title` changes.
    *   **State:** Default, Hover, Active (highlighted).
*   **Form Field Interaction (e.g., Default Tone/Length):**
    *   **Action:** User types, selects an option from a dropdown, or interacts with a slider.
    *   **Feedback:** Field shows a focus state, input appears, dropdown options expand/collapse, selection is highlighted.
    *   **State:** Default, Focused, Edited, Disabled.
*   **"+ Connect New WordPress Site" Button:**
    *   **Action:** User clicks.
    *   **Feedback:** A modal dialog or a new screen appears, prompting for WordPress site details (URL, username, application password).
    *   **State:** Default, Hover, Active.
*   **"Edit" Button (for WP site):**
    *   **Action:** User clicks an `Edit` button for a specific WordPress site.
    *   **Feedback:** A modal or an inline form appears, pre-populated with the site's current connection details for modification.
    *   **State:** Default, Hover, Active.
*   **"Disconnect" Button (for WP site):**
    *   **Action:** User clicks a `Disconnect` button for a specific WordPress site.
    *   **Feedback:** A confirmation modal appears, requesting verification before proceeding with disconnection (e.g., "Are you sure you want to disconnect [Site URL]?"). If confirmed, the site is removed from the list, and a success message appears.
    *   **State:** Default, Hover, Active.
*   **Save Buttons (e.g., "Save AI Settings"):**
    *   **Action:** User clicks.
    *   **Feedback:** The button enters a loading state (e.g., disabled, spinner within button). A success toast or in-page message ("Settings saved successfully!") appears. If validation errors occur, error messages appear next to relevant fields.
    *   **State:** Default, Hover, Active, Loading, Disabled (if no changes or invalid input).
*   **Error States:**
    *   **Feedback:** Input fields with validation errors will typically show a red border/highlight. Clear, concise error messages (e.g., "Invalid URL format," "Please select a tone") will be displayed below the affected input field or as an alert at the top of the content area.
*   **Loading States:**
    *   **Feedback:** Spinners or progress bars will indicate ongoing processes (e.g., connecting a new WordPress site, saving settings). Buttons involved in these processes will be disabled during loading.

### 6. Accessibility Considerations

*   **Keyboard Navigation:**
    *   The tab order will follow a logical sequence: Global Header elements -> Breadcrumbs -> `Settings Navigation` sidebar (top to bottom) -> then into the active `Settings Content Area` (top to bottom, left to right for interactive elements).
    *   All interactive elements (links, buttons, form fields, dropdowns) must be reachable and fully operable using only the keyboard.
*   **Screen Reader Support:**
    *   All headings (`H1`, `H2`) will be used semantically to provide a clear content structure for screen reader users.
    *   Labels will be programmatically associated with their corresponding form input fields using `<label for="...">`.
    *   `aria-current="page"` will be used on the active link within the `Settings Navigation` to inform screen reader users of their current location.
    *   Complex interactive elements (like icon buttons for 'Edit' or 'Disconnect') will have descriptive `aria-label` attributes (e.g., `aria-label="Edit connection for example.com/blog/"`).
    *   Dynamic content updates (e.g., success messages, error alerts, loading states) will use `aria-live="polite"` regions to ensure screen readers announce these changes effectively.
*   **Color Contrast:**
    *   All text (including headings, labels, button text) and interactive UI components (borders, backgrounds of buttons/links) will meet WCAG 2.1 AA contrast ratio requirements (minimum 4.5:1 for regular text, 3:1 for large text or graphical objects).
    *   Focus indicators and active states will also have sufficient contrast to be easily discernible.
*   **Focus Indicators:**
    *   All interactive elements will have clear, distinct visual focus indicators (e.g., a strong border, highlight, or subtle shadow) when navigated via keyboard. This helps users understand which element is currently active.
*   **Alt Text:**
    *   Any functional icons (e.g., in `Edit` or `Disconnect` buttons) will have appropriate `alt` attributes or `aria-label`s.
*   **Error Handling:** Error messages will be clear, concise, and programmatically linked to their associated input fields using `aria-describedby` or similar techniques, allowing screen readers to announce the error when the user focuses on the invalid field.

## UI Elements

- User Profile
- Settings
- Back Button
- Input Field
- Dropdown

