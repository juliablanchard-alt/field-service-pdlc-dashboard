#!/usr/bin/env python3
"""
Send Slack notification for PDLC Dashboard automation
Usage: python3 send_slack_notification.py "message text"
"""
import sys
import subprocess
import json

def send_slack_dm(message):
    """Send a Slack DM to Julia using the Slack MCP server"""
    user_id = "U0601KL1N6R"  # Julia's Slack user ID

    try:
        # Use the MCP Slack tool via subprocess
        # This requires that Claude Code MCP session is running
        result = subprocess.run(
            [
                '/opt/homebrew/bin/claude',
                'tools',
                'call',
                'mcp__plugin_slack_slack__slack_send_message',
                '--channel_id', user_id,
                '--message', message
            ],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            print(f"✅ Slack notification sent successfully")
            return True
        else:
            print(f"❌ Failed to send Slack notification: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("❌ Slack notification timed out")
        return False
    except Exception as e:
        print(f"❌ Error sending Slack notification: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 send_slack_notification.py 'message text'")
        sys.exit(1)

    message = sys.argv[1]
    success = send_slack_dm(message)
    sys.exit(0 if success else 1)
