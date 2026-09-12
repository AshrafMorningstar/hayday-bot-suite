// ============================================================================
//  HAY STAR - Command dispatch table
// ============================================================================

pub mod farm;
pub mod scan;
pub mod info;
pub mod patch;
pub mod hooks;
pub mod native;
pub mod quago;
pub mod spoof;
pub mod misc;

use crate::error::Result;
use crate::session::Session;

/// All recognized commands, their 2-3 letter shortcut, and short description.
pub const COMMANDS: &[(&str, &str)] = &[
    // Master Autonomous Automation Engines
    ("master_cycle", "mc  - 11-step continuous master farm loop (harvest, plant, sell, animals, pets, fish, snipe)"),
    ("master_rotate","mr  - multi-account automatic rotation loop across all profiles"),
    ("auto_heal",    "rc  - auto-recovery: clear disconnect & 'another device' popups, fix loading hangs"),
    ("dashboard",    "db  - interactive master dashboard menu (or 'dash')"),
    ("auto",         "all - execute all commands and systems fully automatically"),
    // Native Farm & Engine Commands
    ("loadnative",  "ln  - load native ARM64 engine module into the game"),
    ("nfields",     "nf  - list current field IDs (must be on farm screen)"),
    ("nplant",      "np  - np [cropId=400001] - plant crop on all fields"),
    ("nharvest",    "nh  - harvest all ready fields"),
    ("wake_pets",   "wp  - wake and feed all pets & sanctuary animals with Wheat (or 'nfp')"),
    ("nsell",       "ns  - ns <slot> [count] [price] [ad] [item] - list item in roadside shop"),
    ("nfarm",       "nfa - nfa [wait=130] [cropId] - auto-farm loop (Ctrl+C to stop)"),
    ("nfdiag",      "nfd - validate native container field enumeration"),
    ("nediag",      "ned - enumeration breakdown diagnostic"),
    ("nping",       "ping- ping the native engine (expect 0xABCD)"),
    ("ndiag",       "ndi - show field-holder objects within 2 hops of gameMode"),
    // Navigation & Lookup Shortcuts
    ("jump",        "j   - j <shop|farm|animals|machines|mine|boat|town|fishing> - camera jump"),
    ("search",      "s   - s <item_name|item_id> - search global ID database"),
    ("ids",         "ids - show Titan Global ID catalog breakdown"),
    ("test",        "tst - run comprehensive diagnostic test suite"),
    // Anti-cheat
    ("nquago",      "nq  - nquago [status|block on|off|spoof on|off] - Quago probe control"),
    ("nstate",      "nst - live game state from Quago telemetry"),
    ("nspoof",      "nsp - nspoof [scan|on|off] - device fingerprint spoof (Galaxy S24 Ultra)"),
    // Memory
    ("info",        "inf - show libg.so base/size/arch/pid"),
    ("read",        "read <type> <offset> [len]"),
    ("write",       "write <type> <offset> <value>"),
    ("dump",        "dump <offset> <length> - hex dump at libg.so offset"),
    ("rabs",        "rabs <abs_addr> <len> - hex dump absolute address"),
    ("wabs",        "wabs <abs_addr> <hexbytes> - write bytes to absolute address"),
    ("export",      "export <name> - look up libg.so export"),
    // Scanner
    ("scan",        "scan <pattern> - AOB scan in libg.so"),
    ("vscan",       "vscan <type> <value> - scan writable memory for typed value"),
    ("vnarrow",     "vnarrow <type> <value> - narrow scan results"),
    ("vlist",       "list current scan results with values"),
    ("vwrite",      "vwrite <value> [index] - write to scan results"),
    ("vreset",      "clear scan results"),
    // Patching
    ("nop",         "nop <offset> <count> - NOP patch at libg.so offset"),
    ("farjump",     "farjump <offset> <target> - 16-byte ARM64 far branch"),
    ("branch",      "branch <offset> <target> [link] - encode B/BL"),
    ("cave",        "cave [size=256] - allocate rwx code cave"),
    ("cavetest",    "test code cave execution via Houdini"),
    ("flushtest",   "test cache flush + inline hook viability"),
    ("gothook",     "test GOT slot redirection"),
    // Hooks
    ("cmdhook",     "hook tryToExecuteCommand and install ring logger"),
    ("cmdlog",      "dump command ring buffer"),
    ("arghook",     "arghook <offset> - hook function and log x0-x7"),
    ("arglog",      "dump argument ring buffer"),
    ("capture",     "capture [secs=12] - capture commands during action"),
    // Misc
    ("dumpso",      "dumpso [path] - dump libg.so to file for Ghidra"),
    ("snap",        "snap [reason] - capture screenshot + logcat + report to error_logs/"),
    ("help",        "h, ? - show this command and shortcut reference guide"),
    ("quit",        "q, exit - exit the loader"),
];

fn run_python_cmd(script: &str, args: &[&str]) -> Result<()> {
    println!("  \x1b[1;36m[>]\x1b[0m Running: python {script} {}", args.join(" "));
    let mut cmd = std::process::Command::new("python");
    cmd.arg(script).args(args);
    match cmd.status() {
        Ok(st) => {
            if !st.success() {
                eprintln!("  \x1b[33m[!] Process returned exit code: {}\x1b[0m", st.code().unwrap_or(1));
            }
        }
        Err(e) => {
            eprintln!("  \x1b[31m[!] Failed to execute python {script}: {e}\x1b[0m");
        }
    }
    Ok(())
}

/// Dispatch a command line to the appropriate handler.
pub fn dispatch(session: &mut Session, line: &str) -> Result<bool> {
    let parts: Vec<&str> = line.trim().split_whitespace().collect();
    if parts.is_empty() { return Ok(true); }

    let cmd = parts[0].to_lowercase();
    let args = &parts[1..];

    match cmd.as_str() {
        // Master Autonomous Automation Engines
        "master_cycle" | "mc" | "master" => farm::cmd_master_cycle(session, args),
        "master_rotate" | "mr" | "rotate" | "acc" => farm::cmd_master_rotate(session, args),
        "auto_heal" | "reconnect" | "rc" | "heal" => farm::cmd_auto_heal(session, args),
        "dashboard" | "dash" | "db" | "launcher" | "menu" => {
            run_python_cmd("launcher.py", args)
        }
        "auto" | "all" | "run" => farm::cmd_master_cycle(session, args),

        // Quick Sector Shortcuts
        "collect_animals" | "ca" => farm::cmd_collect_animals(session, args),
        "feed_animals" | "fa"    => farm::cmd_feed_animals(session, args),
        "collect_machines" | "cm" => farm::cmd_collect_machines(session, args),
        "produce_machines" | "pm" => farm::cmd_produce_machines(session, args),
        "collect_fruits" | "cf"  => farm::cmd_collect_fruits(session, args),
        "chop_all" | "ch"        => farm::cmd_chop_all(session, args),
        "collect_coins" | "cc"   => farm::cmd_collect_coins(session, args),
        "fishing" | "fh"         => farm::cmd_fishing(session, args),
        "mine" | "mn"            => farm::cmd_mine(session, args),
        "sniper" | "sn"          => farm::cmd_sniper(session, args),
        "maintenance" | "mt"     => farm::cmd_maintenance(session, args),
        "account_switch" | "as"  => farm::cmd_account_switch(session, args),
        "config_reload" | "cr"   => farm::cmd_config_reload(session, args),
        "list_ids" | "ids"       => farm::cmd_list_ids(session, args),
        "status" | "st"          => farm::cmd_status(session, args),

        // Quick Tools & Utilities
        "jump" | "j" => {
            let mut pass_args = vec!["j"];
            pass_args.extend_from_slice(args);
            run_python_cmd("engine_bot.py", &pass_args)
        }
        "search" | "s" => {
            let mut pass_args = vec!["s"];
            pass_args.extend_from_slice(args);
            run_python_cmd("engine_bot.py", &pass_args)
        }
        "test" | "tst" => {
            run_python_cmd("tests/test_all.py", &[])
        }

        // Native Farm & Engine Commands
        "loadnative" | "ln" => native::cmd_loadnative(session, args),
        "nfields"    | "nf" => farm::cmd_nfields(session, args),
        "nplant"     | "np" => farm::cmd_nplant(session, args),
        "nharvest"   | "nh" => farm::cmd_nharvest(session, args),
        "wake_pets"  | "wp" | "feed_pets" | "nfp" => {
            println!("  [*] Waking and feeding all pets with Wheat...");
            let _ = std::process::Command::new("python")
                .args(&["engine_bot.py", "--cmd", "wake_pets"])
                .status();
            Ok(())
        },
        "nsell"      | "ns" => farm::cmd_nsell(session, args),
        "nfarm"      | "nfa" | "nfrm" => farm::cmd_nfarm(session, args),
        "nfdiag"     | "nfd" => farm::cmd_nfdiag(session, args),
        "nediag"     | "ned" => farm::cmd_nediag(session, args),
        "nping"      | "ping" => native::cmd_nping(session, args),
        "ndiag"      | "ndi" => native::cmd_ndiag(session, args),

        // Anti-cheat
        "nquago"     | "nq"  => quago::cmd_nquago(session, args),
        "nstate"     | "nst" => quago::cmd_nstate(session, args),
        "nspoof"     | "nsp" => spoof::cmd_nspoof(session, args),

        // Memory
        "info"       | "inf" => info::cmd_info(session, args),
        "read"       => info::cmd_read(session, args),
        "write"      => info::cmd_write(session, args),
        "dump"       => info::cmd_dump(session, args),
        "rabs"       => info::cmd_rabs(session, args),
        "wabs"       => info::cmd_wabs(session, args),
        "export"     => info::cmd_export(session, args),

        // Scanner
        "scan"       => scan::cmd_scan(session, args),
        "vscan"      => scan::cmd_vscan(session, args),
        "vnarrow"    => scan::cmd_vnarrow(session, args),
        "vlist"      => scan::cmd_vlist(session, args),
        "vwrite"     => scan::cmd_vwrite(session, args),
        "vreset"     => scan::cmd_vreset(session, args),

        // Patching
        "nop"        => patch::cmd_nop(session, args),
        "farjump"    => patch::cmd_farjump(session, args),
        "branch"     => patch::cmd_branch(session, args),
        "cave"       => patch::cmd_cave(session, args),
        "cavetest"   => patch::cmd_cavetest(session, args),
        "flushtest"  => patch::cmd_flushtest(session, args),
        "gothook"    => patch::cmd_gothook(session, args),

        // Hooks
        "cmdhook"    => hooks::cmd_cmdhook(session, args),
        "cmdlog"     => hooks::cmd_cmdlog(session, args),
        "arghook"    => hooks::cmd_arghook(session, args),
        "arglog"     => hooks::cmd_arglog(session, args),
        "capture"    => hooks::cmd_capture(session, args),

        // Misc
        "dumpso"     => misc::cmd_dumpso(session, args),
        "snap" | "dumpcrash" => misc::cmd_snap(session, args),
        "help" | "h" | "?" => {
            println!("\n  \x1b[1;36m========================================================================================\x1b[0m");
            println!("  \x1b[1;37mHAY STAR - Commands & 2-3 Letter Short Form Reference\x1b[0m");
            println!("  \x1b[1;36m========================================================================================\x1b[0m");
            println!("  \x1b[1;33m{:<15} {:<80}\x1b[0m", "COMMAND", "SHORTCUT & DESCRIPTION");
            println!("  {}", "-".repeat(88));
            for (name, desc) in COMMANDS {
                println!("    \x1b[1;32m{:<13}\x1b[0m {}", name, desc);
            }
            println!("  \x1b[1;36m========================================================================================\x1b[0m\n");
            Ok(())
        }
        "quit" | "exit" | "q" => {
            println!("  Goodbye.");
            return Ok(false); // signals loop to stop
        }
        _ => {
            println!("  Unknown command: {cmd}  (type 'h' or 'help' for list)");
            Ok(())
        }
    }?;

    Ok(true) // continue loop
}
