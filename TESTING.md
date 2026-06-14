# Thank U Card – Full Testing Documentation

## Overview

This document provides a structured testing process for the **Thank U Card** Django application.

The purpose of this file is to verify that the application works correctly across:

- functionality
- usability
- responsiveness
- authentication
- Google social login
- password reset
- card creation and preview
- AI background and message generation
- basket and checkout flow
- PDF generation and download
- defensive and edge-case behaviour

Thank U Card is a database-backed full-stack Django project. It allows users to create a personalised thank you card, optionally generate a background and/or message with AI, add the card to a basket, complete a test checkout, and download the finished card as a PDF from their account page.

This file is written in a **page-by-page format** so the testing process follows the actual user journey through the website.

---

## Test Setup

### Viewports tested

Testing was completed across the following viewport sizes (Responsivnes in DevTool):

- **Large / Desktop:** 1280×800 and 1440×900
- **Medium / Tablet:** 768×1024 
- **Small / Mobile:** 360×800 and 390×844

### Devices tested

 - Huawei Mate 10 Pro (2017)
 - Samsung Galaxy S25 Ultra
 - The Lenovo Tab M10 Plus
 - Acer Swift 1 SF114-32


### Browsers tested

- Google Chrome
- Firefox

### DevTools used during testing

- **Elements panel**: check layout, overflow, field visibility, responsive classes and hidden elements
- **Console**: check JavaScript errors during form interaction, preview updates and auto-refresh
- **Network tab**: check CSS, JavaScript, images, AI generation requests, Stripe redirects and PDF downloads
- **Application / Storage**: check session behaviour, basket persistence and authentication state
- **Lighthouse**: check performance, accessibility, best practices and SEO
- **Device toolbar**: check tablet and mobile responsiveness

### Accounts used during testing

Three accounts should be prepared:

- **User A** – standard registered user with saved cards
- **User B** – second standard registered user to test account isolation
- **Admin** – Django superuser for `/admin/` checks

### External / third-party services tested

- Django authentication
- Django password reset email flow
- Google login via django-allauth
- OpenAI image/message generation flow
- Cloudinary image storage
- Celery/Redis background task flow
- Stripe test checkout flow
- PDF generation and download

### Test card data used

The following test data was used to cover normal and edge-case behaviour:

| Field | Normal test value | Edge-case values |
|---|---|---|
| Recipient name | `Mum` | blank, 20 characters, over 20 characters, emoji |
| Message | `Thank you for everything.` | blank, 150 characters, over 150 characters, special characters |
| Recipient type | Friend / Family / Teacher / Colleague | each option tested |
| Theme | Any available theme | each option tested |
| Colour | Each available colour | no colour selected if possible |
| Element | Each available element | no element selected if possible |
| No message checkbox | Unticked | ticked, ticked then unticked |

### Pass / Fail notes

- Use **Pass** only when the expected result is met exactly.
- Use **Fail** when the result differs from the expected result.
- Use **Pass after debugging** when an issue was found and fixed.
- Record visual issues under **Known Issues / Improvements** if the function works but needs polish.

---

# Global Cross-Page Checks

These checks apply to every page using the base template.

## Large Screen — Desktop ≥ 1024px

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| GX-L-01 | Page loads | Open each main page | Page renders without server error | Pass |
| GX-L-02 | Navbar layout | Inspect navbar on all pages | Navbar is aligned, readable and consistent | Pass |
| GX-L-03 | Auth-based navbar | Compare logged-out and logged-in navbar | Logged-out users see login/register; logged-in users see account/logout options | Pass |
| GX-L-04 | Home link | Click on home button | User returns to home page | Pass |
| GX-L-05 | Footer layout | Scroll to footer | Footer is visible, readable and not overlapping content | Pass |
| GX-L-06 | Flash messages | Trigger success/error messages | Messages display clearly and do not break layout | Pass |
| GX-L-07 | Console check | Navigate through all pages with Console open | No recurring JavaScript errors | Pass |
| GX-L-08 | Static assets | Hard refresh pages | CSS, JS, favicon and images load correctly | Pass |
| GX-L-09 | Keyboard navigation | Use Tab through links, buttons and forms | Focus is visible and follows a logical order | Pass |
| GX-L-10 | Browser zoom | Check pages at 90%, 100%, 110% and 125% | No clipping, overlap or unusable controls | Pass |

## Medium Screen — Tablet around 768px

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| GX-M-01 | Layout transition | Resize from desktop to 768px | Columns stack or resize cleanly | Pass |
| GX-M-02 | Navbar wrapping | Inspect navbar at tablet width | Navbar does not overflow or push buttons awkwardly | Pass |
| GX-M-03 | Touch usability | Use touch simulation | Buttons and links are easy to tap | Pass |
| GX-M-04 | Footer wrapping | Inspect footer | Footer content wraps neatly | Pass |
| GX-M-05 | Horizontal overflow | Swipe horizontally | No unexpected horizontal scroll | Pass |

## Small Screen — Mobile ≤ 414px

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| GX-S-01 | No horizontal scroll | Open all pages at 360px and swipe sideways | No sideways overflow | Pass |
| GX-S-02 | Mobile navbar | Open and close mobile nav if present | Menu works correctly and remains usable | Pass |
| GX-S-03 | Button tap targets | Tap buttons near the edges | Buttons respond reliably | Pass |
| GX-S-04 | Text wrapping | Inspect long labels, messages and buttons | Text wraps naturally without clipping | Pass |
| GX-S-05 | Mobile spacing | Scroll from top to bottom | No sections collapse into each other | Pass |

---

# PAGE 1 — Home / Card Builder

The home page contains the main card creation form, live preview, AI background generation, AI message generation and card actions.

## Large Screen — Desktop ≥ 1024px

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| HP-L-01 | Home page loads | Open `/` | Hero, demo notice and card builder render correctly | Pass |
| HP-L-02 | Hero readability | Inspect hero text and background | Text is readable and not interrupted by background image | Pass |
| HP-L-03 | Demo notice | Inspect student project notice | Notice is visible and clearly warns about demo use | Pass |
| HP-L-04 | Step 1 options display | Inspect recipient type, theme, colour, element and no-message checkbox | All fields are visible and labelled correctly | Pass |
| HP-L-05 | Step 2 preview display | Inspect preview card | Card preview panel is visible and centred | Pass |
| HP-L-06 | Step 3 actions display | Inspect Save, Reset and Add to basket buttons | Buttons are visible, aligned and usable | Pass |
| HP-L-07 | Recipient live preview | Type a recipient name | Preview updates to show `Dear [name]` | Pass |
| HP-L-08 | Message live preview | Type a message | Preview updates immediately with the typed message | Pass |
| HP-L-09 | Character counters | Type in recipient and message fields | Counters update live and show correct character count | Pass |
| HP-L-10 | Clear message button | Type a message then click Clear message | Message field clears and preview returns to placeholder | Pass |
| HP-L-11 | No-message checkbox hides text | Tick `Card without message` | Recipient field, message field, message box, message buttons and note are hidden | Pass |
| HP-L-12 | No-message checkbox restores text | Untick `Card without message` | Recipient field, message field, buttons, note and preview message area return | Pass |
| HP-L-13 | No-message state persists after submit | Tick no-message and submit allowed action | Saved card remains without message | Pass |
| HP-L-14 | Generate background button | Select options and click Generate background with AI | Generation begins and progress UI appears | Pass |
| HP-L-15 | Background auto-refresh | Wait during generation | Page auto-refreshes while generation is in progress | Pass |
| HP-L-16 | Generated background display | Wait until background is ready | Generated image appears in the card preview | Pass |
| HP-L-17 | AI background limit | Generate more than allowed daily limit | User receives clear limit message and generation is blocked | Pass |
| HP-L-18 | Generate/improve message | Enter or leave message field then click Generate / Improve message | AI-generated/improved message appears in message field and preview | Pass |
| HP-L-19 | Generate message hidden when no-message selected | Tick no-message | Generate/improve and Clear message buttons are hidden | Pass |
| HP-L-20 | Save card | Create card and click Save | Card is saved and user receives success feedback | Pass |
| HP-L-21 | Reset page | Click Reset | Form and preview return to default clean state | Pass |
| HP-L-22 | Add to basket | Create card and click Add to basket | Card is added to basket or user is redirected to login if required | Pass |
| HP-L-23 | Submit with blank fields | Leave optional fields blank and save | App handles blank recipient/message safely according to no-message setting | Pass |
| HP-L-24 | Special characters | Enter emoji, quotes, ampersands and HTML-like text | Text displays safely and does not execute as code | Pass |
| HP-L-25 | Very long input handling | Try entering over max length | Field blocks extra characters or form shows validation error | Pass |
| HP-L-26 | Console cleanliness | Use all home page interactions with Console open | No JS errors occur | Pass |

## Medium Screen — Tablet around 768px

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| HP-M-01 | Builder column reflow | Inspect home builder at 768px | Step panels stack or resize cleanly | Pass |
| HP-M-02 | Preview card fit | Inspect preview card | Card fits without overflow or distortion | Pass |
| HP-M-03 | Form fields | Use all form fields | Inputs, selects and checkbox remain usable | Pass |
| HP-M-04 | AI buttons | Inspect Generate buttons | Buttons remain centred and do not stretch awkwardly | Pass |
| HP-M-05 | Action buttons | Inspect Save/Reset/Add buttons | Buttons stay aligned and tappable | Pass |

## Small Screen — Mobile ≤ 414px

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| HP-S-01 | Mobile home fit | Open home at 360px | No horizontal scroll | Pass |
| HP-S-02 | Step order | Scroll through page | Step 1, Step 2 and Step 3 appear in logical order | Pass |
| HP-S-03 | Preview scaling | Inspect card preview | Card scales properly and remains readable | Pass |
| HP-S-04 | Text fields | Focus fields and type | Mobile keyboard does not make the form unusable | Pass |
| HP-S-05 | No-message behaviour | Tick and untick no-message | Fields and buttons hide/show correctly on mobile | Pass |
| HP-S-06 | Button stacking | Inspect all buttons | Buttons stack or centre cleanly, no long stretched awkward buttons | Pass |
| HP-S-07 | Auto-refresh visual | Start background generation | Progress message remains visible and usable | Pass |

---

# PAGE 2 — Login Page

## Large Screen — Desktop ≥ 1024px

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| LG-L-01 | Login page loads | Open login page | Form renders correctly | Pass |
| LG-L-02 | Empty submit | Submit blank form | Validation prevents login | Pass |
| LG-L-03 | Invalid credentials | Enter incorrect email/password | Error message shown and login blocked | Pass |
| LG-L-04 | Valid credentials | Enter valid User A details | User logs in successfully | Pass |
| LG-L-05 | Redirect after login | Log in from login page | User is redirected correctly | Pass |
| LG-L-06 | Login after protected action | Try Add to basket while logged out then log in | User can continue safely after login | Pass |
| LG-L-07 | Register link | Click register/create account link | Register page opens | Pass |
| LG-L-08 | Forgot password link | Click password reset link | Password reset request page opens | Pass |
| LG-L-09 | Google login button | Inspect Google sign-in option | Button is visible and clearly labelled | Pass |
| LG-L-10 | Console check | Use login interactions with Console open | No JavaScript errors | Pass |

## Medium / Small Screen

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| LG-R-01 | Responsive layout | Open login page on tablet and mobile | Login panel fits and remains readable | Pass |
| LG-R-02 | Input usability | Focus email/password fields | Fields remain visible and usable with keyboard | Pass |
| LG-R-03 | Button fit | Inspect login, Google and password reset buttons | Buttons remain tappable and do not overflow | Pass |

---

# PAGE 3 — Register Page

## Large Screen — Desktop ≥ 1024px

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| RG-L-01 | Register page loads | Open register page | Form renders correctly | Pass |
| RG-L-02 | Empty submit | Submit blank form | Required field errors display | Pass |
| RG-L-03 | Invalid email | Enter malformed email | Email validation blocks submission | Pass |
| RG-L-04 | Existing email | Register with email already used | Clear error shown | Pass |
| RG-L-05 | Password mismatch | Enter different passwords | Form blocks registration | Pass |
| RG-L-06 | Weak password | Enter weak password | Django password validation message shown | Pass |
| RG-L-07 | Valid registration | Enter valid details | Account is created successfully | Pass |
| RG-L-08 | Post-register flow | Complete registration | User is logged in or redirected according to project flow | Pass |
| RG-L-09 | Login link | Click existing-account/login link | Login page opens | Pass |

## Medium / Small Screen

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| RG-R-01 | Responsive form | Open page on tablet/mobile | Form fields fit screen | Pass |
| RG-R-02 | Error wrapping | Trigger multiple errors | Error messages wrap cleanly | Pass |
| RG-R-03 | Password fields | Focus password fields on mobile | Inputs remain visible and usable | Pass |

---

# PAGE 4 — Google Sign-In Flow

Google authentication is tested separately because it uses django-allauth and an external provider.

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| GA-01 | Google login route | Click Google login button | User is redirected to Google authentication page | Pass |
| GA-02 | Cancel Google login | Start Google login then cancel | User returns safely to site without account being created incorrectly | Pass |
| GA-03 | Successful Google login | Complete Google login with valid account | User is signed in successfully | Pass |
| GA-04 | Existing email handling | Use Google email matching an existing account if supported | App handles account connection safely | Pass |
| GA-05 | New Google account | Sign in with Google account not used before | Account is created or linked according to allauth settings | Pass |
| GA-06 | Navbar after Google login | Return to site after Google login | Navbar shows logged-in state | Pass |
| GA-07 | Account page access | Open account page after Google login | Account page loads correctly | Pass |
| GA-08 | Logout after Google login | Click logout | User is logged out and protected pages are blocked | Pass |
| GA-09 | Production callback URL | Test deployed site Google login | Redirect URI works without mismatch error | Pass |
| GA-10 | Local callback URL | Test local site if configured | Local Google login works or is documented as unavailable | Pass |

---

# PAGE 5 — Password Reset Request

## Large Screen — Desktop ≥ 1024px

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| PRF-L-01 | Reset page loads | Open password reset form | Page renders correctly | Pass |
| PRF-L-02 | Empty email | Submit empty form | Browser or Django validation blocks submit | Pass |
| PRF-L-03 | Invalid email format | Enter invalid email | Error shown | Pass |
| PRF-L-04 | Existing account email | Submit email linked to account | User sees generic email-sent confirmation | Pass |
| PRF-L-05 | Non-existing email | Submit email not linked to account | Same generic confirmation shown; no account leakage | Pass |
| PRF-L-06 | Email delivered | Check inbox/test email backend | Password reset email is sent correctly | Pass |
| PRF-L-07 | Email subject/content | Inspect email | Subject and body are clear and include valid reset link | Pass |
| PRF-L-08 | Back to login link | Click login link | Login page opens | Pass |

## Medium / Small Screen

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| PRF-R-01 | Responsive layout | Open reset page on tablet/mobile | Panel fits and text remains readable | Pass |
| PRF-R-02 | Email input usability | Tap email field and submit | Form is usable on touch devices | Pass |

---

# PAGE 6 — Password Reset Email Sent Page

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| PRD-01 | Confirmation page | Submit password reset request | Email sent/check inbox page loads | Pass |
| PRD-02 | Privacy wording | Read confirmation message | Message does not reveal whether account exists | Pass |
| PRD-03 | Back to login | Click login CTA | Login page opens correctly | Pass |
| PRD-04 | Responsive fit | View on tablet/mobile | Page remains centred and readable | Pass |

---

# PAGE 7 — Password Reset Confirm Page

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| PRC-01 | Valid reset link | Open valid reset link from email | New password form appears | Pass |
| PRC-02 | Blank passwords | Submit both password fields blank | Validation errors display | Pass |
| PRC-03 | Mismatched passwords | Enter two different passwords | Reset is blocked | Pass |
| PRC-04 | Weak password | Enter invalid weak password | Django password validation error shown | Pass |
| PRC-05 | Successful reset | Enter valid matching passwords | Password is updated successfully | Pass |
| PRC-06 | Login with old password | Try old password after reset | Old password no longer works | Pass |
| PRC-07 | Login with new password | Try new password | User can log in successfully | Pass |
| PRC-08 | Expired/invalid link | Open malformed or expired link | Safe invalid-link message shown | Pass |
| PRC-09 | Request new link | Click request new link CTA | User returns to reset request page | Pass |
| PRC-10 | Responsive fit | Test valid and invalid states on mobile | Layout remains usable | Pass |

---

# PAGE 8 — Password Reset Complete Page

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| PRCOMP-01 | Completion page | Complete password reset | Completion page loads | Pass |
| PRCOMP-02 | Login link | Click login CTA | Login page opens | Pass |
| PRCOMP-03 | Responsive fit | View on tablet/mobile | Page remains readable and centred | Pass |

---

# PAGE 9 — Basket Page

The basket page displays cards selected for checkout.

## Large Screen — Desktop ≥ 1024px

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| BK-L-01 | Basket empty state | Open basket with no items | Friendly empty basket message shown | Pass |
| BK-L-02 | Add card to basket | Add one card from home page | Card appears in basket | Pass |
| BK-L-03 | Basket preview image | Inspect basket card image | Background image displays correctly if generated | Pass |
| BK-L-04 | Basket text preview | Inspect card message in basket | Recipient/message displayed correctly if message enabled | Pass |
| BK-L-05 | No-message basket state | Add no-message card to basket | Basket does not show unwanted message area | Pass |
| BK-L-06 | Multiple cards | Add more than one card | All cards appear separately | Pass |
| BK-L-07 | Remove item | Click remove from basket | Item is removed and total updates | Pass |
| BK-L-08 | Remove last item | Remove final card | Empty basket state appears | Pass |
| BK-L-09 | Continue creating | Click continue/create another card | User returns to home builder | Pass |
| BK-L-10 | Checkout button | Click checkout/test checkout | User moves to Stripe/test checkout flow | Pass |
| BK-L-11 | Logged-out access | Open basket while logged out | User is redirected or shown safe empty/protected state | Pass |
| BK-L-12 | User isolation | Log in as User B and open User A basket URL if possible | User B cannot access User A basket items | Pass |

## Medium / Small Screen

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| BK-R-01 | Basket layout on tablet | Inspect at 768px | Basket rows stack cleanly | Pass |
| BK-R-02 | Basket layout on mobile | Inspect at 360px | No horizontal overflow | Pass |
| BK-R-03 | Remove button size | Tap remove button | Button is easy to tap and not too long/awkward | Pass |
| BK-R-04 | Checkout button placement | Inspect checkout CTA | Button is centred and visible | Pass |

---

# PAGE 10 — Preview Page

The preview page displays a card before final checkout or after selecting a card from another page.

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| PV-01 | Preview page loads | Open preview for an existing card | Card preview renders correctly | Pass |
| PV-02 | Background image | Inspect generated card | Background image is visible and not distorted | Pass |
| PV-03 | Message overlay | Inspect message area | Text appears in correct position and remains readable | Pass |
| PV-04 | No-message card | Open preview for no-message card | Message box is hidden | Pass |
| PV-05 | Edit card link | Click edit card | User is taken to edit page for that card | Pass |
| PV-06 | Add to basket from preview | Click Add to basket | Card is added to basket | Pass |
| PV-07 | Invalid card ID | Manually open non-existing preview URL | Safe 404 or redirect is shown | Pass |
| PV-08 | Other user card | Try to preview another user’s private card by URL | Access denied, redirect or 404 | Pass |
| PV-09 | Mobile preview | Open at mobile width | Card scales correctly without overflow | Pass |

---

# PAGE 11 — Edit Card Page

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| EC-01 | Edit page loads | Open edit page for own saved card | Existing card data appears in form | Pass |
| EC-02 | Edit recipient | Change recipient name and save | Updated recipient appears in preview/basket/account | Pass |
| EC-03 | Edit message | Change message and save | Updated message appears correctly | Pass |
| EC-04 | Clear message | Use Clear message button | Message clears and preview updates | Pass |
| EC-05 | Toggle no-message on | Tick no-message and save | Message fields/buttons hide and saved card has no message | Pass |
| EC-06 | Toggle no-message off | Untick no-message and save | Message fields/buttons return | Pass |
| EC-07 | Generate improved message | Click Generate / Improve message | Message updates safely | Pass |
| EC-08 | Regenerate background | Change options and generate background | New background generation begins | Pass |
| EC-09 | Save changes | Click save changes | Existing card updates instead of creating duplicate unexpectedly | Pass |
| EC-10 | Add edited card to basket | Save then add to basket | Updated version is added/displayed | Pass |
| EC-11 | Other user edit URL | Log in as User B and open User A edit URL | Access denied or 404 | Pass |
| EC-12 | Mobile edit layout | Open edit page on mobile | Form and preview remain usable | Pass |

---

# PAGE 12 — Stripe / Test Checkout Flow

This is a demo project, so checkout must only use Stripe test details.

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| ST-01 | Checkout with empty basket | Try checkout with no basket items | Checkout is blocked and user remains safe | Pass |
| ST-02 | Checkout with one card | Add card then click checkout | Stripe checkout opens | Pass |
| ST-03 | Checkout with multiple cards | Add multiple cards and checkout | Stripe checkout includes expected basket/order total | Pass |
| ST-04 | Demo warning | Inspect checkout/payment messaging before redirect | User is warned not to use real payment details | Pass |
| ST-05 | Successful test payment | Use Stripe test success card | User returns to success page | Pass |
| ST-06 | Failed/declined card | Use Stripe test declined card | Error is handled by Stripe and no order is completed | Pass |
| ST-07 | Cancel checkout | Click back/cancel from Stripe | User returns to site without completed order | Pass |
| ST-08 | Duplicate checkout submit | Double-click checkout if possible | No duplicate order/payment created | Pass |
| ST-09 | Webhook/order status | Complete payment and check order/card status | Purchased card is marked complete/final as expected | Pass |
| ST-10 | Basket after success | Return after successful payment | Basket is cleared or completed items are no longer active | Pass |
| ST-11 | Direct success URL access | Manually open success URL without payment | App handles safely and does not create fake order | Pass |
| ST-12 | Mobile checkout redirect | Start checkout on mobile | Redirect is usable and returns correctly | Pass |

---

# PAGE 13 — Account Page

The account page displays saved/purchased cards and PDF download links.

## Large Screen — Desktop ≥ 1024px

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| AC-L-01 | Account protection | Open account page while logged out | User is redirected to login | Pass |
| AC-L-02 | Account page load | Log in and open account | Account page renders correctly | Pass |
| AC-L-03 | Empty account state | Use account with no cards | Friendly empty-state message shown | Pass |
| AC-L-04 | Saved card list | Save card and open account | Saved card appears | Pass |
| AC-L-05 | Purchased card list | Complete checkout and open account | Purchased card appears as completed/final | Pass |
| AC-L-06 | Card preview link | Click preview on account card | Correct card preview opens | Pass |
| AC-L-07 | Edit saved card | Click edit on saved card if allowed | Edit page opens | Pass |
| AC-L-08 | No edit after purchase | Inspect purchased/final card | Final/purchased card cannot be edited if locked | Pass |
| AC-L-09 | PDF download visible | Complete checkout and wait for PDF | Download PDF button/link appears | Pass |
| AC-L-10 | PDF not ready state | Open account before final PDF is ready | Clear pending/processing message shown | Pass |
| AC-L-11 | Download PDF | Click download PDF | PDF downloads or opens correctly | Pass |
| AC-L-12 | PDF content | Open downloaded PDF | PDF contains correct card background/message or no-message layout | Pass |
| AC-L-13 | User isolation | Log in as User B | User B cannot see User A cards or PDFs | Pass after debugging |
| AC-L-14 | Long list of cards | Account with many cards | Layout remains readable and scrollable | Pass |
| AC-L-15 | Logout link | Click logout from account/nav | User logs out successfully | Pass |

## Medium / Small Screen

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| AC-R-01 | Account mobile layout | Open account at 360px | No horizontal overflow | Pass |
| AC-R-02 | Card row stacking | Inspect saved card rows | Text and buttons stack neatly | Pass |
| AC-R-03 | PDF button usability | Tap download button | Button is easy to tap | Pass |
| AC-R-04 | Long card titles/text | Inspect cards with longer messages | Content wraps safely | Pass |

---

# PAGE 14 — PDF Generation and Download

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| PDF-01 | PDF generated after payment | Complete successful test checkout | Final PDF generation starts or completes | Pass |
| PDF-02 | PDF ready status | Refresh account page after completion | PDF ready/download state appears | Pass |
| PDF-03 | PDF with message | Download card with recipient/message | PDF shows background and readable message area | Pass |
| PDF-04 | PDF without message | Download no-message card | PDF does not show empty message box | Pass |
| PDF-05 | PDF image quality | Open downloaded PDF | Background appears clear and not badly stretched | Pass |
| PDF-06 | PDF file name | Check downloaded file | File name is meaningful and safe | Pass |
| PDF-07 | PDF permission | Try accessing another user’s PDF link | Access blocked or file not exposed | Pass after debugging |
| PDF-08 | Missing image fallback | Test card where background failed/missing | PDF generation fails gracefully or uses safe fallback | Pass |
| PDF-09 | Re-download | Download same PDF multiple times | File downloads reliably without changing order state | Pass |
| PDF-10 | Mobile PDF download | Download PDF on mobile | Download/open behaviour works according to browser/device | Pass |

---

# PAGE 15 — Custom 404 Page

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| E404-01 | Invalid route | Open non-existing URL | Custom 404 page loads | Pass |
| E404-02 | Styling consistency | Inspect 404 page | Page matches site design | Pass |
| E404-03 | Recovery link | Click home link | User returns to home page | Pass |
| E404-04 | Invalid object URL | Open non-existing card/preview URL | Safe 404 or redirect shown | Pass |
| E404-05 | Mobile 404 | View at 360px | Page remains centred and readable | Pass |

---

# Django CRUD and Permission Testing

## Card CRUD

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| CRUD-CARD-01 | Create card | Complete form and save | New Card record is created | Pass |
| CRUD-CARD-02 | Read own card | Open preview/account for own card | Card data displays correctly | Pass |
| CRUD-CARD-03 | Update own card | Edit and save own card | Existing card updates correctly | Pass |
| CRUD-CARD-04 | Add card to basket | Add saved card to basket | BasketItem is created correctly | Pass |
| CRUD-CARD-05 | Remove from basket | Remove card | BasketItem is removed | Pass |
| CRUD-CARD-06 | Finalise card after payment | Complete checkout | Card/order marked final or purchased | Pass |
| CRUD-CARD-07 | Prevent editing final card | Try editing purchased/locked card | Edit is blocked if project rules require locking | Pass |
| CRUD-CARD-08 | Other user read attempt | User B opens User A private card URL | Access denied, redirect or 404 | Pass |
| CRUD-CARD-09 | Other user edit attempt | User B opens User A edit URL | Access denied, redirect or 404 | Pass |
| CRUD-CARD-10 | Deleted/invalid card URL | Open removed/non-existing card URL | Safe 404 or redirect | Pass |

## Basket and Order Rules

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| CRUD-BASKET-01 | Basket created for user | Add first card to basket | Basket exists for logged-in user/session | Pass |
| CRUD-BASKET-02 | Multiple items | Add several cards | Basket stores each item correctly | Pass |
| CRUD-BASKET-03 | Duplicate add behaviour | Add same card twice | App handles according to rules: prevents duplicate or displays duplicate intentionally | Pass |
| CRUD-BASKET-04 | Basket ownership | Switch user accounts | Basket contents are isolated by user | Pass |
| CRUD-BASKET-05 | Checkout creates order | Complete test checkout | Order/payment record created correctly | Pass |
| CRUD-BASKET-06 | Cancel does not create final order | Cancel Stripe checkout | Order/card not falsely marked as paid | Pass |

---

# JavaScript Testing

The JavaScript controls live preview, character counters, hiding message fields/buttons and auto-refresh during generation.

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| JS-01 | Script loads | Open home page with Console open | `main.js` loads without syntax errors | Pass |
| JS-02 | Safe fallback | Open pages without card builder elements | No JS errors from missing elements | Pass |
| JS-03 | Recipient counter initial state | Open home/edit page | Counter shows current field length | Pass |
| JS-04 | Recipient counter update | Type recipient name | Counter updates live | Pass |
| JS-05 | Message counter initial state | Open home/edit page | Counter shows current message length | Pass |
| JS-06 | Message counter update | Type message | Counter updates live | Pass |
| JS-07 | Live recipient preview | Type recipient | Preview updates immediately | Pass |
| JS-08 | Live message preview | Type message | Preview updates immediately | Pass |
| JS-09 | Clear message | Click clear button | Message clears and preview updates | Pass |
| JS-10 | No-message hide | Tick no-message | Message fields, preview box, message buttons and note hide | Pass |
| JS-11 | No-message show | Untick no-message | Message fields, preview box, buttons and note return | Pass |
| JS-12 | Progress auto-refresh | Trigger background generation | Page refreshes automatically while generation is active | Pass |
| JS-13 | No duplicate listeners | Interact repeatedly | No duplicate updates or console errors | Pass |
| JS-14 | JSHint validation | Run JSHint on JS file | No syntax errors; ES6 setting accepted | Pass |

---

# AI Generation Testing

## Background Generation

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| AI-BG-01 | Required input handling | Generate background with normal selected options | Request accepted and generation begins | Pass |
| AI-BG-02 | Prompt options used | Change theme/colour/element and generate | Background reflects selected options as closely as possible | Pass |
| AI-BG-03 | Progress state | Start generation | User sees generating/progress state | Pass |
| AI-BG-04 | Auto-refresh | Wait during progress | Page refreshes until status changes | Pass |
| AI-BG-05 | Success state | Generation completes | Background image appears in preview | Pass |
| AI-BG-06 | Failure state | Simulate failed task/API error if possible | User receives safe error/fallback message | Pass |
| AI-BG-07 | Daily limit | Exceed 3 generations in 24h | Generation is blocked and limit message shown | Pass |
| AI-BG-08 | Cloudinary persistence | Refresh page after successful generation | Image remains visible and not lost | Pass |
| AI-BG-09 | Heroku persistence | Restart/redeploy if possible | Image remains available via Cloudinary | Pass |
| AI-BG-10 | Fast repeated clicks | Click generate repeatedly | Duplicate tasks are prevented or handled safely | Pass |

## Message Generation

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| AI-MSG-01 | Generate from blank message | Click Generate / Improve message with blank message | A suitable thank-you message is generated | Pass |
| AI-MSG-02 | Improve existing message | Enter rough message then generate | Message is improved and remains within field limit | Pass |
| AI-MSG-03 | Uses selected context | Change recipient/theme options then generate | Message tone fits the selected context | Pass |
| AI-MSG-04 | Hidden for no-message | Tick no-message | Generate message button is hidden and not usable | Pass |
| AI-MSG-05 | Sensitive data notice | Inspect note near message tools | User is warned not to enter private/sensitive data | Pass |

---

# Form Validation and Edge Cases

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| EDGE-01 | Blank recipient | Leave recipient blank | App handles optional recipient safely | Pass |
| EDGE-02 | Blank message with message enabled | Leave message blank and no-message unticked | Placeholder or validation appears according to project rules | Pass |
| EDGE-03 | No-message card | Tick no-message and submit | Card saves without message | Pass |
| EDGE-04 | Toggle no-message repeatedly | Tick/untick several times | UI remains stable and correct | Pass |
| EDGE-05 | Recipient max length | Enter 20 characters | Accepted and counter displays 20/20 | Pass |
| EDGE-06 | Recipient over max length | Try more than 20 characters | Blocked or validation error shown | Pass |
| EDGE-07 | Message max length | Enter 150 characters | Accepted and counter displays 150/150 | Pass |
| EDGE-08 | Message over max length | Try more than 150 characters | Blocked or validation error shown | Pass |
| EDGE-09 | Spaces-only input | Enter only spaces | Saved output does not create ugly blank message state | Pass |
| EDGE-10 | Emoji input | Enter emoji in message | Emoji display safely or validation handles it | Pass |
| EDGE-11 | Very long generated background wait | Keep page open during long generation | User is not left with broken UI | Pass |
| EDGE-12 | Missing background image | Remove image or use failed card | Preview, basket and account do not crash | Pass |
| EDGE-13 | Browser refresh after submit | Refresh after Save/Add to basket | No unexpected duplicate card or duplicate basket item | Pass |
| EDGE-14 | Browser Back after checkout | Use Back after completed payment | Completed order state remains consistent | Pass |

---

# Security / Defensive Behaviour Testing

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| SEC-01 | Protected account page | Open account while logged out | Redirected to login | Pass |
| SEC-02 | Protected basket/checkout | Attempt basket/checkout while logged out | Redirected or blocked safely | Pass |
| SEC-03 | CSRF on forms | Submit all forms normally | Forms work with CSRF protection | Pass |
| SEC-04 | URL tampering card preview | Change card ID in URL | Other user card is not exposed | Pass |
| SEC-05 | URL tampering edit | Change edit URL to another user’s card | Access denied or 404 | Pass |
| SEC-06 | URL tampering PDF | Try another user’s PDF URL | Access denied or file unavailable | Pass after debugging |
| SEC-07 | Password reset privacy | Submit existing and non-existing email | Same generic response shown | Pass |
| SEC-08 | HTML/script input | Submit HTML-like text | Code does not execute | Pass |
| SEC-09 | Admin protection | Open `/admin/` while logged out | Admin login required | Pass |
| SEC-10 | Normal user admin access | Log in as standard user and open `/admin/` | Access denied | Pass |

---

# Browser Behaviour / Recovery Testing

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| BR-01 | Refresh home builder | Enter form data and refresh | App behaves according to saved/current card state | Pass |
| BR-02 | Refresh during generation | Start generation and refresh manually | Generation state remains safe | Pass |
| BR-03 | Back after add to basket | Add to basket then use Back | Basket state remains consistent | Pass |
| BR-04 | Back after remove | Remove basket item then use Back | Removed item does not reappear as active | Pass |
| BR-05 | Multi-tab editing | Open same card edit page in two tabs | Final saved state remains consistent | Pass |
| BR-06 | Logout then protected page | Logout then use Back to account | Protected data is not accessible | Pass |

---

# CSS / Visual Quality Testing

| Test ID | What to test | Test steps | Expected result | Pass / Fail |
|---|---|---|---|---|
| CSS-01 | Global background | Inspect main body/background on all pages | Background image/layer does not interrupt text | Pass |
| CSS-02 | Container opacity | Inspect main containers | Text remains readable over background | Pass |
| CSS-03 | Button hierarchy | Compare primary/secondary buttons | Main buttons stand out; secondary buttons are clear | Pass |
| CSS-04 | AI animated buttons | Hover/click AI buttons | Animation works and does not break layout | Pass |
| CSS-05 | Hidden class behaviour | Toggle no-message | Hidden elements fully disappear without leaving awkward gaps | Pass |
| CSS-06 | Preview card sizing | Inspect preview across devices | Card keeps aspect ratio and remains centred | Pass |
| CSS-07 | Basket buttons | Inspect basket on medium widths | Buttons stay centred and do not become long awkward bars | Pass |
| CSS-08 | Account card rows | Inspect account rows | Text and buttons align cleanly | Pass |
| CSS-09 | PDF/download buttons | Inspect account download actions | Buttons are visible and consistent | Pass |
| CSS-10 | Text contrast | Inspect headings, labels, notices and buttons | Contrast is readable on all backgrounds | Pass |
| CSS-11 | Error messages | Trigger validation errors | Errors are readable and spaced correctly | Pass |
| CSS-12 | Mobile spacing | Inspect all pages at 360px | No squeezed, clipped or overlapping content | Pass |

---

### PDF Download Access Testing - Bug 16

During testing, the PDF download process was reviewed to ensure that purchased card files could not be accessed directly without application-level permission checks.

Originally, the account page linked directly to the Cloudinary PDF file. This was identified as a potential access-control issue because a copied file URL could be opened outside the account page.

The download process was updated to use a protected Django route instead of exposing the direct Cloudinary file URL. The route checks that the user is logged in, owns the card, the card has been paid for, and a PDF file exists before returning the file.

This was manually tested by confirming that paid users could download their own PDFs from the account page, while direct access through the application route was restricted by the card ownership and payment checks.

**Result:** Passed.

---

# Validation Testing

This section documents the validation checks completed for the Thank U Card project. Validation was carried out across HTML, CSS, JavaScript, Python, and Lighthouse testing to confirm that the deployed application follows good coding standards, accessibility expectations, and browser best practices.

Validation screenshots are stored in the project under:

```text
assets/validation/
```

The folder is split into separate subfolders for each validation type:

```text
assets/validation/css/
assets/validation/html/
assets/validation/js/
assets/validation/python/
assets/validation/lighthouse/
```

This structure keeps all validation evidence together while separating each type of test clearly.

---

## HTML Validation

HTML validation was completed using the official W3C Markup Validation Service:

```text
https://validator.w3.org/
```

All main templates were checked and any reported issues were reviewed and corrected. The final HTML validation results showed no errors.

During validation, semantic structure was reviewed across the main pages, including headings, forms, navigation, account pages, basket pages, preview pages, and authentication pages. Some heading structure and form accessibility issues were updated during this stage to improve both validation quality and Lighthouse accessibility results.

Evidence screenshots are stored in:

```text
assets/validation/html/
```

---

## CSS Validation

CSS validation was completed using the official W3C CSS Validation Service:

```text
https://jigsaw.w3.org/css-validator/
```

The project CSS files were tested, including the global stylesheet and page-specific stylesheet.

The final CSS validation returned no errors. Some warnings were shown by the validator. These warnings were reviewed and were related mainly to modern CSS features, CSS variables, and vendor-specific properties such as `-webkit-backdrop-filter`. These warnings were accepted because they relate to browser support and modern styling rather than invalid CSS.

CSS validation evidence is stored in:

```text
assets/validation/css/
```

---

## JavaScript Validation

JavaScript validation was completed using JSHint:

```text
https://jshint.com/
```

The main JavaScript file was tested after adding the required configuration comment:

```javascript
/* jshint esversion: 6 */
```

The final JavaScript validation completed successfully with no errors. The script was also updated to use the `defer` attribute in the base template to reduce render-blocking behaviour during Lighthouse testing.

JavaScript validation evidence is stored in:

```text
assets/validation/js/
```

---

## Python Validation

Python validation was completed using the Code Institute PEP8 validator:

```text
https://pep8ci.herokuapp.com/
```

Python files were checked for PEP8 compliance. Any reported formatting issues were reviewed and corrected. Final checks showed the Python files passing validation.

Python validation evidence is stored in:

```text
assets/validation/python/
```

---

## Lighthouse Testing

Lighthouse testing was carried out using Chrome DevTools on the deployed Heroku application. The main user-facing pages were tested in both desktop and mobile views.

Tested pages included:

- Home page
- Home page while logged in
- Login page
- Register page
- Account page
- Basket page
- Card preview page from account
- Card preview page from basket
- Edit card page

Lighthouse testing reviewed:

- Performance
- Accessibility
- Best Practices
- SEO


### Lighthouse Results

### Desktop Lighthouse Results

Desktop Lighthouse results were strong across the application. The final desktop tests showed high scores, with Accessibility, Best Practices, and SEO reaching 100 on the tested pages after improvements were made.

Performance scores were lower on image-heavy pages such as the Home page, Edit Card page, and Preview pages. This was expected because the project is visual by design. The core purpose of Thank U Card is to generate and preview personalised card images, so large visual assets and generated card previews are essential functionality rather than decorative extras.

#### Desktop

| Page | Performance | Accessibility | Best Practices | SEO |
|---|---:|---:|---:|---:|
| Home | 80 | 100 | 100 | 100 |
| Home - Logged In | 77 | 100 | 100 | 100 |
| Login | 92 | 100 | 100 | 100 |
| Register | 97 | 100 | 100 | 100 |
| Account | 90 | 100 | 100 | 100 |
| Basket | 96 | 100 | 100 | 100 |
| Account Card Preview | 88 | 100 | 100 | 100 |
| Basket Card Preview | 87 | 100 | 100 | 100 |
| Edit Card | 77 | 100 | 100 | 100 |

### Mobile Lighthouse Results

Mobile Lighthouse results showed lower Performance scores than desktop results. This was expected because Lighthouse applies stricter throttling for mobile testing and because the application relies heavily on images, generated backgrounds, Google Fonts, FontAwesome icons, and Cloudinary-hosted media.

Accessibility, Best Practices, and SEO scores were strong after improvements were made. Several tested mobile pages achieved 100 for Accessibility, Best Practices, and SEO.

#### Mobile

| Page | Performance | Accessibility | Best Practices | SEO |
|---|---:|---:|---:|---:|
| Home | 64 | 100 | 100 | 100 |
| Home - Logged In | 68 | 100 | 100 | 100 |
| Login | 70 | 100 | 100 | 100 |
| Account | 70 | 100 | 100 | 100 |
| Basket | 73 | 100 | 100 | 100 |
| Account Card Preview | 70 | 95 | 77 | 100 |
| Basket Card Preview | 69 | 100 | 100 | 100 |
| Edit Card | 63 | 100 | 100 | 100 |

### Lighthouse Improvements Made

Several improvements were made following Lighthouse feedback:

- JavaScript was loaded with the `defer` attribute to reduce render-blocking behaviour.
- Select field labels were corrected so each label points to the correct form field.
- Empty preview headings were updated with visually hidden accessible text.
- Contrast was improved for the student demo note and navigation text.
- Form accessibility was reviewed across the Home and Edit Card pages.
- Browser-extension warnings were investigated and confirmed not to be part of the application source code.

### Accepted Lighthouse Warnings

Some Lighthouse warnings were reviewed and accepted as reasonable trade-offs for the project:

- Image delivery warnings were accepted because generated card previews and visual backgrounds are central to the application.
- Performance warnings related to Cloudinary-hosted generated images were accepted because Cloudinary is required for production media storage.
- External font and icon warnings were accepted because Google Fonts and FontAwesome support the visual design of the site.
- Some CSS warnings were accepted because shared CSS files are used across templates to maintain consistent styling.

Lighthouse evidence screenshots are stored in:

```text
assets/validation/lighthouse/
```
---

## Summary

Validation confirmed that the final project code meets the required standards for the scope of the project. HTML, CSS, JavaScript, and Python validation were completed successfully, with no final errors reported.

Lighthouse testing confirmed that the application is accessible, SEO-friendly, and usable across desktop and mobile devices. Remaining performance limitations were reviewed and accepted because Thank U Card is an image-focused application where generated card previews are essential to the user journey.

---

# Testing Summary

Thank U Card was tested across desktop, tablet and mobile using:

- manual interaction testing
- responsive layout testing
- authentication testing
- Google social login testing
- password reset testing
- basket and checkout testing
- PDF generation/download testing
- JavaScript behaviour testing
- AI generation edge-case testing
- security and permission checks
- validation tools
- Lighthouse audits

The testing covers both the happy path and defensive scenarios, including:

- invalid form input
- no-message card creation
- failed or delayed AI generation
- protected routes
- URL tampering
- account isolation
- basket edge cases
- checkout cancellation
- PDF readiness
- mobile usability
- long text and special characters

This testing process demonstrates that the application is functional, responsive, defensive, and appropriate for a full-stack Django student project.
