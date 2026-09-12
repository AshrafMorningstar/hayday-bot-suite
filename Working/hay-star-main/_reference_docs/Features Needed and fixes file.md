
- The privacy page now says everything that leaves your PC. Newspaper Sniper
  plans a second time, and that snapshot is the newspaper page rather than your
  farm: up to 200 of the adverts it shows you, each with the item, its price
  and quantity, the advertising farm's level and the farm id printed on the
  advert. It is used to choose which adverts to open and is not kept. No
  earlier version of the policy said so.
- The wiki's spending page is honest about coins. Newspaper Sniper buys at the
  seller's price with no price filter, so what bounds it is your own per-product
  limits and its purchases-per-pass cap. It was missing from the list of
  modules that spend.
- The loader now says which failure stopped it. A rotated certificate, an
  unreachable server, a timeout and no network reached you as one sentence;
  they are now told apart, which is what a support case turns on.
- Eleven Manual actions had no button on any page, including the only way to
  claim a Farm Pass reward that asks you to choose. They are wired, and one
  truck action's default was a truck id that is not a truck.
- Applying a save no longer writes it under a running game. The Accounts page
  stops the engine and the game first, the way its own Stop and Clear data
  buttons always did, and refuses the write if the game will not stop.
- A licence that was only suspended told you it had been revoked, and quit.
  It now says what actually happened.


- The privacy page now says everything that leaves your PC. Newspaper Sniper
  plans a second time, and that snapshot is the newspaper page rather than your
  farm: up to 200 of the adverts it shows you, each with the item, its price
  and quantity, the advertising farm's level and the farm id printed on the
  advert. It is used to choose which adverts to open and is not kept. No
  earlier version of the policy said so.
- The wiki's spending page is honest about coins. Newspaper Sniper buys at the
  seller's price with no price filter, so what bounds it is your own per-product
  limits and its purchases-per-pass cap. It was missing from the list of
  modules that spend.
- The loader now says which failure stopped it. A rotated certificate, an
  unreachable server, a timeout and no network reached you as one sentence;
  they are now told apart, which is what a support case turns on.
- Eleven Manual actions had no button on any page, including the only way to
  claim a Farm Pass reward that asks you to choose. They are wired, and one
  truck action's default was a truck id that is not a truck.
- Applying a save no longer writes it under a running game. The Accounts page
  stops the engine and the game first, the way its own Stop and Clear data
  buttons always did, and refuses the write if the game will not stop.
- A licence that was only suspended told you it had been revoked, and quit.
  It now says what actually happened.

- The privacy page now says everything that leaves your PC. Newspaper Sniper
  plans a second time, and that snapshot is the newspaper page rather than your
  farm: up to 200 of the adverts it shows you, each with the item, its price
  and quantity, the advertising farm's level and the farm id printed on the
  advert. It is used to choose which adverts to open and is not kept. No
  earlier version of the policy said so.
- The wiki's spending page is honest about coins. Newspaper Sniper buys at the
  seller's price with no price filter, so what bounds it is your own per-product
  limits and its purchases-per-pass cap. It was missing from the list of
  modules that spend.
- The loader now says which failure stopped it. A rotated certificate, an
  unreachable server, a timeout and no network reached you as one sentence;
  they are now told apart, which is what a support case turns on.
- Eleven Manual actions had no button on any page, including the only way to
  claim a Farm Pass reward that asks you to choose. They are wired, and one
  truck action's default was a truck id that is not a truck.
- Applying a save no longer writes it under a running game. The Accounts page
  stops the engine and the game first, the way its own Stop and Clear data
  buttons always did, and refuses the write if the game will not stop.
- A licence that was only suspended told you it had been revoked, and quit.
  It now says what actually happened.

- "New" no longer closes the client. With any module page open - Fields,
  Machines, Animals, Trucks or Roadside Shop, the five whose page carries a
  table - starting a new config crashed outright. The page installs a status
  refresher that holds its table by pointer; starting a new config tore the
  page down and then refreshed the plan, which called that refresher straight
  into the table it had just deleted. The teardown now drops the refresher
  with the widgets it points at, which is where that belonged: the other
  teardown path already did exactly this, and only this one was missing it.
  Deleting a config took the same route and could crash the same way.
- A test now opens a module page, presses New and checks the page came down
  cleanly. Without the fix that test dies where the client did.

- Farm configs from 2.5.203 and earlier open again. The fishing switch was
  renamed in 2.5.204 without a migration step, so every saved config failed the
  schema check instead of being carried forward. The switch now crosses with its
  value intact. Its new lure list arrives empty, and empty means no fish is
  taken: taking one spends a lure, and a config written before the list existed
  never said which bait to burn - so pick one in Fishing before it fishes again.

- The plan's "Needs attention" strip opens closed: one line saying how many
  things need attention, the detail one click away. A plan that could not make
  a few dozen rows printed a line for each and pushed the module list off the
  bottom of the pane.
- Newspaper Sniper walks every advertised farm again. Skipping a farm whose
  advertised product sat at its limit turned "also scan other advertisements"
  upside down: a farm selling something you never asked for was always visited,
  while one advertising your own product was refused - and its other slots,
  readable only on arrival, are what the run is after. The run still ends when
  nothing you buy is open, and "max sellers / pass" is still the throttle.
- Roadside Shop prices are set by choice, not by typing a number. The ceiling
  depends on the product and its stack size, so one number was the maximum for
  one row and below the floor for the next. Price now has its own line and its
  own Set: highest, 75%, half, or lowest, resolved against each row's own
  ceiling.
- A planting pass that the game refuses says so. It used to report "no empty
  field to plant" while the same line counted empty ground, because a crop the
  farm has not unlocked is refused as a whole request, not field by field.
- Fields: in "cover shortages first, fill the rest with X", X now takes every
  empty field. Its own stock target no longer caps that fill, which is what the
  mode has always promised. Ground was left bare whenever X sat near its target
  and the short crops were off the Fields crop list.

- One production chain, read the same way everywhere. Every module that asks
  the plan for an item - a product to keep stocked, a truck order to fill from
  production, an animal's feed, a shop listing, a visitor's request - now
  checks the whole chain under it against what this plan actually produces,
  by the exact rule the planner uses for ground. A ticked row shows its
  verdict on the row ("in plan", "blocked", "from stock only") with the reason
  on hover, and the strip above the plan names the first broken link and
  carries the click that mends it: [Add Sheep], [Grow Cotton in Fields],
  [Add Machines].
- Two wrong answers that rule replaced. A recipe short of a crop the Fields
  list omits was assumed fine (it was not: the list is the allowlist for
  ground). An intermediate not ticked in Machines was reported as missing (it
  is not: the plan makes a missing intermediate straight from the recipe).
  With Fields off, crops are still sown for other modules' shortages, so that
  no longer reads as a missing module either.
- The panel's answer is pinned to the planner's rule by tests, so the two
  cannot drift apart again without a build failing.


- Farm Config: a module's page could come up blank and stay blank. A repaint
  hold placed around the page swap restored whatever state it found, so a page
  built while something else was holding repaints off never got them back.
  The hold is gone; the page is drawn every time.

- Farm Config bulk edit is direct again: select rows, type the numbers in the
  bar, press Set. Every selected row is ticked and given those numbers. The
  bar sits in two lines so it fits the smallest window.

- Feed Animals action no longer refuses a partially-built barn. It used to
  insist on "completed
- Farm Config, steadied. Two quick clicks on a row's check box no longer take
  the tick back (a double-click was counted as a third toggle). The table no
  longer shivers on every tick, the bulk bar no longer pushes it up and down
  as rows are selected, and ticking no longer drops the keyboard focus into
  the row's number.
- The bulk bar copies the current row's numbers to the selected rows instead
  of carrying its own set of boxes, so it fits at every window size. Labels
  and column headers are shorter; the page fits the smallest window.
- Opening a module no longer marks the config as edited; Save lights up only
  for a real change.

- Farm Config, tidied. The paragraph above the plan is one line now (cadence
  and module count); the full explanation is on hover. Every module opens the
  same way: one hint line, its switches, its table. Ticking a row no longer
  makes the table jump, opening a module no longer flashes a window, and the
  standing "Chores may spend coins" warning is gone.
- The "Check against" account view is removed: the stock it showed was the
  last snapshot, not live, and it earned its space with nobody.

- Farm Config is rebuilt around one table per module: tick a product and its
  target, queue, price or limit appear on that same row, with no second list to
  keep in step. Priority is the # cell (type a position, Alt+Up/Down, or the
  right-click menu). Select several rows and one bar ticks, unticks or writes
  the same number into all of them. Every module's switches sit in one grid
  above its table.
- Each product shows what it needs, hop by hop, down to crops and animals; each
  animal shows what it eats and gives.
- Check against an account: pick one HDX has run and every table gains a Now
  column with what that farm holds, read against the row's own numbers ("55
  owned · keep 20 · 35 sellable"). Under the table, the last pass on that farm
  explains itself in the planner's own words, so "why is it not selling" is
  answered next to the row instead of in the log.
- Plan warnings are links to the module they name.
- Your light/dark choice is kept per Windows account now, not in the install
  folder; set it once more with the top-right button and it stays.
- Two USB-only files left the download; HDX reaches emulators over the network
  only, so installs and updates are smaller.
- Loader 2.5.18 comes with this release and installs itself.
- A refused sign-in shows a short reference, like (ref: 7QK2M4): quote it and
  support can see exactly which of several causes it was.
- Stops the game stuttering while HDX works. The native runtime no longer
  re-reads the game's memory map on every game-thread step and hands the frame
  back after each one, so bulk readouts and collections that froze the farm for
  a third of a second now run at full frame rate and finish up to ten times
  sooner.
- Loader 2.5.16 updates itself: it downloads a newly published loader by its
  signed hash, verifies it, replaces its own executable and restarts on the
  chosen channel. The Telegram button stays the first install and the fallback.
  A wrong PC date or time is now named as such, not as a signature failure.
- Fixes native farm readiness on translated Android processes, so a loaded farm
  is no longer mistaken for a stalled launch.
- Reports an operator Stop as a stop instead of a lost game connection, and
  never lets a Stop be missed by the scheduler.
- Multi mode gives up on an account list that keeps failing instead of retrying
  it forever, and names an unreadable Multi-Config instead of hiding it.
- Carries older saved configs forward: the Smart-Limit ceilings widened in
  2.5.181 now apply to configs saved before it, and per-crop field limits are
  migrated explicitly instead of being silently reinterpreted.
- Restores the "Only orders with a listed product" truck filter as its own mode
  (Farm Config schema 20), so a truck order you wanted is never deleted by the
  stricter filter.
- Tells the three device-credential failures apart instead of one generic
  "restart Windows" message.
- Refreshes the reviewed dependency and build-toolchain baseline.
- Stops the game stuttering while HDX works. The native runtime no longer
  re-reads the game's memory map on every game-thread step and hands the frame
  back after each one, so bulk readouts and collections that froze the farm for
  a third of a second now run at full frame rate and finish up to ten times
  sooner.
- Loader 2.5.16 updates itself: it downloads a newly published loader by its
  signed hash, verifies it, replaces its own executable and restarts on the
  chosen channel. The Telegram button stays the first install and the fallback.
  A wrong PC date or time is now named as such, not as a signature failure.
- Fixes native farm readiness on translated Android processes, so a loaded farm
  is no longer mistaken for a stalled launch.
- Reports an operator Stop as a stop instead of a lost game connection, and
  never lets a Stop be missed by the scheduler.
- Multi mode gives up on an account list that keeps failing instead of retrying
  it forever, and names an unreadable Multi-Config instead of hiding it.
- Carries older saved configs forward: the Smart-Limit ceilings widened in
  2.5.181 now apply to configs saved before it, and per-crop field limits are
  migrated explicitly instead of being silently reinterpreted.
- Restores the "Only orders with a listed product" truck filter as its own mode
  (Farm Config schema 20), so a truck order you wanted is never deleted by the
  stricter filter.
- Tells the three device-credential failures apart instead of one generic
  "restart Windows" message.
- Refreshes the reviewed dependency and build-toolchain baseline.
- Uses the native provider's exact process identity instead of rediscovering the
  game through emulator process-tree heuristics, preventing false identity-change
  failures during account startup.
- Keeps large tree and bulk-operation readouts lightweight while preserving
  bounded game-thread batches, reducing frame stalls on very large farms.
- Avoids repeating newspaper readiness work and temporarily isolates an
  unresponsive production target so the rest of the configured pass can proceed.
- Uses the native provider's exact process identity instead of rediscovering the
  game through emulator process-tree heuristics, preventing false identity-change
  failures during account startup.
- Keeps large tree and bulk-operation readouts lightweight while preserving
  bounded game-thread batches, reducing frame stalls on very large farms.
- Avoids repeating newspaper readiness work and temporarily isolates an
  unresponsive production target so the rest of the configured pass can proceed.
- Makes account Grab reliable when Windows refuses or races a temporary path,
  and shows the real local error when a transfer cannot start.
- Recovers account switches, farm returns and interrupted native connections
  without replaying completed game actions.
- Starts and stops more predictably by separating game exits, cancelled stops,
  connection loss and farm-readiness failures.
- Keeps large farms responsive during tree, animal, machine and other bulk
  operations, while loading large farm lists in ordered batches.
- Collects ready output from every eligible machine and balances production
  across both Sugar/Feed Mills and all five Smelters.
- Counts each Feed Mill queue slot as the three feed units it produces.
- Applies the truck product list to the whole order: unwanted orders are cleared
  before missing products are queued.
- Uses configured crop amounts as real stock targets; selected-crop mode still
  plants only the chosen crop.
- Avoids stale planting after a full-silo harvest and lets the Roadside Shop
  sell eligible stock before the next harvest attempt.
Stable · 2.5.190
- Keeps the authenticated native connection alive while Manual mode is idle;
  only an incomplete protocol frame retains a bounded receive deadline.
- Reports a lost native connection once and marks that engine unavailable,
  instead of cascading into an unrelated initialization error.
- Fixes native startup on Windows by parsing the guest's typed readiness status
  independently of ADB's LF-to-CRLF conversion.
- Removes redundant root-identity subprocesses from tight native startup polls
  after the root generation has already been proven.

- Completes the native runtime transition; the retired Frida runtime is not
  part of the client or emulator launch path.
- Makes LDPlayer root startup and native-runtime staging transactional. Files
  are hash/owner/mode verified before activation, and retries cannot inherit a
  half-written runtime.
- Replaces LDPlayer's silently truncating binary-stdin path with one
  memory-only, device-acknowledged ADB sync transaction. Provider, guest and
  token-bearing configuration bytes are still hash-verified before activation.
- Reports the provider's exact startup rejection instead of hiding every guest
  load failure behind one generic message.
- Completes the native runtime transition; the retired Frida runtime is not
  part of the client or emulator launch path.
- Makes LDPlayer root startup and native-runtime staging transactional. Files
  are hash/owner/mode verified before activation, and retries cannot inherit a
  half-written runtime.
- Replaces LDPlayer's silently truncating binary-stdin path with one
  memory-only, device-acknowledged ADB sync transaction. Provider, guest and
  token-bearing configuration bytes are still hash-verified before activation.
- Reports the provider's exact startup rejection instead of hiding every guest
  load failure behind one generic message.
- Uses the Stable/Beta lane authenticated by the loader handoff and rejects an
  invalid lane before any API request.
- Reports local clock drift separately from an expired license so users receive
  the correct corrective action.
- Shows the real free-trial outcome: already used, unverifiable device evidence,
  or an identity conflict that needs support review.
- Lets a customer enter a paid activation key when an old trial binding cannot
  continue, without deleting their local accounts or settings.

- Strengthens device sign-in so a session becomes active only after the enrolled
  device credential has completed its protected proof.
- Improves legitimate device continuity across ordinary hardware changes while
  keeping device changes, trial history and machine restrictions server-controlled.
- Makes transient session recovery reliable without treating an expired license as
  a recoverable connection problem. Update through the loader.

- Session refreshes now recover the exact committed, device-sealed response
  after a lost HTTP reply instead of entering a spent-token retry loop.
- Permanent refresh results stop the retry timer and request a clean sign-in;
  transient network/service failures retain the timed retry path.
- Refresh runs every three minutes inside the five-minute minimum session TTL,
  leaving a two-minute recovery margin.
- Machine production no longer enters the missing-ingredient diamond fallback;
  unavailable work is skipped without slowing successful production.
- Fresh emulators can initialize account storage without a manual first launch,
  and an unavailable emulator stops cleanly instead of retrying every account.
- Manual Market adds Buy All. Listing and sold-slot collection now use every
  live shop slot instead of an old ten-slot assumption.
- Inventory and Info follow the farm currently being visited.
- Large farms can complete tree, machine, mining, field, placement and tutorial
  batches without old small-farm cutoffs.
- Production resolves every required crop and intermediate dependency in the
  same planning pass when possible.
- Smart mining follows the live random diamond count and stops at its configured
  target or tool allowance.
- Newspaper purchases cover the complete supported visited shop and safely skip
  offers that changed before purchase.
- Chop All now includes Dandelion and Peanut Bush objects.
- Action, object, response and command capacities now share one verified
  client/server contract.
- Multi Mode now stops immediately when its selected emulator, ADB transport
  or client runtime is unavailable. It reports the unavailable environment
  once instead of retrying every account in a tight loop; genuinely retryable
  game-start failures retain their bounded clean-launch attempts.

- Multi Mode now stops immediately when its selected emulator, ADB transport
  or client runtime is unavailable. It reports the unavailable environment
  once instead of retrying every account in a tight loop; genuinely retryable
  game-start failures retain their bounded clean-launch attempts.

- Separates an expired license from an expired or superseded secure session.
  Routine server restarts and token rotation can no longer close a paid user's
  client with a false license-expired message.
- A stale session is now recovered silently through the enrolled device key.
  Genuine expired, suspended and revoked licenses remain terminal.

- Fixes an empty Multi Mode summary for farms that fit the current filter
  criteria but cannot be started (for example, by being already running or
  offline). The summary now shows all matching accounts and reports only running
  or unreachable ones as unavailable.
- Rebuilds the game-start boundary around one event-driven lifecycle observer.
  HDX now advances only after the live game itself reports a complete, stable
  farm or creator state; host polling and guessed startup delays are not used.
- Normal account launches no longer load account-creator UI code. Creator-only
  dialog support is a separately verified component and is loaded only after a
  real first-launch screen has been detected.
- Runtime delivery is one immutable three-part signed bundle tied to this exact
  client and game version. Incomplete, mixed-version and obsolete bundle shapes
  are rejected instead of being interpreted through a compatibility path.
- Duplicate session/script attachment is now rejected at the engine boundary,
  preventing an accidental retry from leaking or replacing a live runtime.
- Later scheduled passes now re-arm that same typed native farm boundary. The
  redundant signed-action/frame-counter polling loop has been removed, leaving
  one readiness authority and eliminating its cold-start and idle-pass tax.

- Fixes a game that was visibly open on the farm while HDX remained at
  `waiting for game runtime`. The startup monitor and the client now use one
  typed readiness contract, so an already-ready farm cannot be rejected merely
  because the game's one-byte started flag crossed the agent boundary as a
  number instead of a true/false value.
- A finished LDPlayer game process that remains only as an inert zombie no
  longer blocks the next clean launch or forces an emulator restart. HDX still
  refuses to continue while any live game or tracer process remains.

- Local device-bound trial reservations remain tied to the initial device
  signature. An expired local trial no longer causes the client to fail
  authentication when the user enrolls a new valid device and enters a new
  paid key.
- The loader ensures that paid users who enter an activation key after
  an expired local trial never inherit trial-session identity and can start
  their licensed game normally.
- When a paid key is present, the client will not attempt to enroll the
  device into a new trial and will not leak legacy trial binding into future
  server exchanges.
- HDX now reads the real free trial status directly from the live server.
  Local trial-expiration checks are retained only as cached sentinels for
  offline continuity. When the server reports a live trial, the client stays
  entitled and never rejects a valid device or key.
- Fixes an edge case where the user would see trial-expired while their
  device-bound trial was still active. The server remains the single source
  of truth for paid vs trial entitlement.

- The "Use Google Play" button now reliably redirects to the external
  Google Play app instead of performing a failed in-app purchase attempt
  through the embedded Play Store WebView.
- After redirection, the user is correctly brought back to the HDX client
  and can continue using their paid subscription normally.

- Introduces the Production tab, a new dedicated workspace that consolidates
  all machine-production and crop-farming operations.
- Key features:
  - "Production Feed" shows active, pending, and backlogged machine and
    crop tasks.
  - Batch controls for initiating and completing large production runs.
  - Real-time progress tracking and management.
- This replaces the old "Orders" tab, providing a more organized, powerful,
  and transparent interface for managing farm production workflows.

- Start now remains Stop for the whole live run. A shared runner cleanup had
  accidentally left two separate running flags; the worker changed one while
  the card read the other, so the UI could say `starting` and immediately look
  idle even though the engine thread was still active.
- Startup now proves the actual own-farm object and its stable identity. It no
  longer waits on a short-lived internal startup counter that can legitimately
  remain zero on a fully rendered farm, which caused a healthy first launch to
  sit at `waiting for game runtime`.
- A completed game command whose requested screen/state takes too long to
  settle stays local to that feature. HDX restarts the game only when the
  process/session is gone or a queued command saw no game-thread boundary at
  all, so one slow module no longer destroys an otherwise live run.
- Session rotation no longer mistakes a late response from the previous token
  for a dead licence, and replacing an expired old binding with a new activation
  key no longer carries an old close signal into the new session.

- Fixes the start hang for real this time. The readiness check that proves the
  farm is up counts two good readings in a row, and it was throwing that count
  away every time a status read came back empty -- which happens under load, when
  the game is busy. On a loaded machine the two good readings could never land
  back to back, so a farm that was genuinely up and playable was declared 'never
  settled' and the account was relaunched over and over. Empty and partial reads
  are now treated as a dropped frame and ignored, so the count survives them.

- The "Use Google Play" button now reliably redirects to the external
  Google Play app instead of performing a failed in-app purchase attempt
  through the embedded Play Store WebView.
- After redirection, the user is correctly brought back to the HDX client
  and can continue using their paid subscription normally.

- Fixes a start that could sit for four minutes doing nothing and then kill a
  perfectly good game. The check that proves the farm is ready times itself from
  the moment it first recognises that farm, and it recognises it by an internal
  identity — so whenever that identity kept changing, or the farm never quite
  registered, the timer restarted forever and nothing could end the wait. It now
  also measures from the moment the game itself reports it has started, which
  nothing restarts: an account that will not settle is given up on in about a
  minute and a half, with the reason named, and the next clean launch begins.

- HDX now starts a clean game for each new account, avoiding a mixed-state
  startup that could fail to present the main game board.
- The client now recognises its own main game UI after startup and immediately
  launches into the farm, using the same robust detection as in the creator
  sandbox.
- Any game or creator dialog currently open is automatically closed before the
  first scheduled pass, ensuring a consistent and predictable starting state.
- Fixes a long-running issue where new accounts would remain stuck at a
  "waiting for game" state due to persistent, uncleared dialogs and mixed
  session states.
- Fixes a start that could sit for four minutes doing nothing and then kill a
  perfectly good game. The check that proves the farm is ready times itself from
  the moment it first recognises that farm, and it recognises it by an internal
  identity — so whenever that identity kept changing, or the farm never quite
  registered, the timer restarted forever and nothing could end the wait. It now
  also measures from the moment the game itself reports it has started, which
  nothing restarts: an account that will not settle is given up on in about a
  minute and a half, with the reason named, and the next clean launch begins.

- HDX now starts a clean game for each new account, avoiding a mixed-state
  startup that could fail to present the main game board.
- The client now recognises its own main game UI after startup and immediately
  launches into the farm, using the same robust detection as in the creator
  sandbox.
- Any game or creator dialog currently open is automatically closed before the
  first scheduled pass, ensuring a consistent and predictable starting state.
- Fixes a long-running issue where new accounts would remain stuck at a
  "waiting for game" state due to persistent, uncleared dialogs and mixed
  session states.
- Fixes the start hang for real this time. The readiness check that proves the
  farm is up counts two good readings in a row, and it was throwing that count
  away every time a status read came back empty -- which happens under load, when
  the game is busy. On a loaded machine the two good readings could never land
  back to back, so a farm that was genuinely up and playable was declared 'never
  settled' and the account was relaunched over and over. Empty and partial reads
  are now treated as a dropped frame and ignored, so the count survives them.
  
- A licence that stops being valid while HDX is open now says so and closes,
  instead of quietly retrying for as long as the app is left running. An expiry, a
  suspension or revocation, or a licence moved to another PC is reported by the
  next authenticated call — which happens even while idle, because the session
  keeps itself fresh. HDX names the reason, stops every card so the seat is
  released, and exits.
- The game check now asks one question: is this the supported Hay Day version and
  ABI. It used to also inspect the installed APK files, which refused perfectly
  good installs: the same version is packaged differently depending on where it
  was installed from. That inspection is gone.
- Fixes games that died or froze seconds after the farm appeared. HDX attached
  with Frida's default settings, one of which takes over the game's own crash
  handling — so the game, running translated on the emulator, could no longer
  install the fault handler it depends on, and a fault it normally absorbs killed
  it or left the picture frozen. On one loaded emulator the old setting lost the
  game three times in six runs; the new one never lost it.
- Fixes a startup that failed about one time in five for no real reason. The
  check that confirms the farm is alive watched a counter that, by the game's own
  design, stops about ten seconds after the farm loads; on a slow start HDX looked
  only after it had stopped and rejected a healthy farm. It now accepts a farm
  whose counter has run at all, and still waits out one that never started.

- A licence that stops being valid while HDX is open now says so and closes,
  instead of quietly retrying for as long as the app is left running. An expiry, a
  suspension or revocation, or a licence moved to another PC is reported by the
  next authenticated call — which happens even while idle, because the session
  keeps itself fresh. HDX names the reason, stops every card so the seat is
  released, and exits.
- The game check now asks one question: is this the supported Hay Day version and
  ABI. It used to also inspect the installed APK files, which refused perfectly
  good installs: the same version is packaged differently depending on where it
  was installed from. That inspection is gone.
- Fixes games that died or froze seconds after the farm appeared. HDX attached
  with Frida's default settings, one of which takes over the game's own crash
  handling — so the game, running translated on the emulator, could no longer
  install the fault handler it depends on, and a fault it normally absorbs killed
  it or left the picture frozen. On one loaded emulator the old setting lost the
  game three times in six runs; the new one never lost it.
- Fixes a startup that failed about one time in five for no real reason. The
  check that confirms the farm is alive watched a counter that, by the game's own
  design, stops about ten seconds after the farm loads; on a slow start HDX looked
  only after it had stopped and rejected a healthy farm. It now accepts a farm
  whose counter has run at all, and still waits out one that never started.
  