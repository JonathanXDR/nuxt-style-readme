package main

import "os/exec"

// Uses osascript because pomo ships no dependencies and macOS has no notify-send.
func notifySend(msg string) {
	exec.Command("osascript", "-e", "display notification \""+msg+"\"").Run()
}
