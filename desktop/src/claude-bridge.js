/**
 * Claude API Bridge for Arsenal Transfer War Room
 * =================================================
 * Handles communication between the Electron renderer and Claude API.
 * Runs in the main process with full Node.js access.
 */

const Anthropic = require("@anthropic-ai/sdk");

const SYSTEM_PROMPT = `You are Arsenal FC's AI-powered sporting director assistant, embedded in the Transfer War Room desktop app. You help analyze transfers, update player data, and provide tactical insights.

IMPORTANT: You respond in a specific JSON format so the app can parse your answers and update the dashboard automatically.

Your response MUST be valid JSON with this structure:
{
  "message": "Your human-readable response text here (markdown supported)",
  "data_updates": {
    "remove_targets": ["Player Name"],
    "add_targets": [
      {
        "name": "Player Name",
        "age": 22,
        "position": "CB",
        "nationality": "Country",
        "market_value_m": 40.0,
        "wage_weekly_k": 80.0,
        "contract_expiry": "2029-06-30",
        "current_club": "Club Name",
        "stats": {
          "appearances": 20, "goals": 2, "assists": 1, "minutes": 1700,
          "progressive_passes": 30, "progressive_carries": 20,
          "tackles_won": 25, "interceptions": 18, "aerials_won": 35,
          "pass_completion_pct": 87.0
        },
        "eye_test": "Scouting assessment...",
        "strengths": ["Strength 1", "Strength 2"],
        "weaknesses": ["Weakness 1"],
        "estimated_fee_m": 40.0,
        "priority_score": 75,
        "role": "rotation"
      }
    ],
    "update_targets": [
      {
        "name": "Existing Player Name",
        "updates": {
          "market_value_m": 50.0,
          "status": "signed_by_rival",
          "rival": "Man City"
        }
      }
    ],
    "update_budget": null,
    "add_sell_candidate": null,
    "remove_sell_candidate": null
  }
}

RULES:
- "message" is ALWAYS required. Write a clear, insightful response.
- "data_updates" is optional. Only include it when the user asks to change data.
- If the user just asks a question, set "data_updates" to null.
- For new targets, provide realistic stats and a thorough eye_test assessment.
- priority_score: 80+ = Priority 1, 60-79 = Priority 2, below 60 = Priority 3.
- All fees in EUR millions. Wages in GBP thousands per week.
- Be opinionated like a real sporting director. Take strong stances.
- Reference real stats, real transfer rumors, and real tactical analysis.

CURRENT CONTEXT (provided with each message):
The user will send you the current state of the transfer plan including all targets, sell candidates, budget, and financial data. Use this to give contextually relevant answers.`;

let client = null;
let conversationHistory = [];

function initClient(apiKey) {
  client = new Anthropic({ apiKey });
  conversationHistory = [];
}

function isReady() {
  return client !== null;
}

async function chat(userMessage, currentData) {
  if (!client) {
    throw new Error("API key not configured. Go to Settings to add your Anthropic API key.");
  }

  // Build context from current data
  let context = "";
  if (currentData) {
    const buys = (currentData.transfer_plan?.buy_recommendations || [])
      .map(b => `${b.player} (${b.position}, ${b.age}) - Score: ${b.priority_score}/100 - €${b.estimated_fee_m}m - ${b.current_club}`)
      .join("\n  ");
    const sells = (currentData.transfer_plan?.sell_recommendations || [])
      .map(s => `${s.player} - €${s.projected_fee_m}m - ${s.urgency}`)
      .join("\n  ");
    const fin = currentData.financial_report?.budget_overview || {};

    context = `\n\n--- CURRENT PLAN STATE ---
Budget: €${fin.base_budget_m}m | Sales Revenue: €${fin.sale_revenue_m}m | Available: €${fin.total_available_m}m | Spend: €${fin.total_spend_m}m | Remaining: €${fin.remaining_m}m

Buy Targets:
  ${buys || "(none)"}

Sell Candidates:
  ${sells || "(none)"}
--- END STATE ---`;
  }

  // Add user message to history
  conversationHistory.push({
    role: "user",
    content: userMessage + context,
  });

  // Keep last 20 messages to avoid token overflow
  if (conversationHistory.length > 20) {
    conversationHistory = conversationHistory.slice(-20);
  }

  const response = await client.messages.create({
    model: "claude-sonnet-4-5-20250929",
    max_tokens: 4096,
    system: SYSTEM_PROMPT,
    messages: conversationHistory,
  });

  const assistantText = response.content[0].text;

  // Add assistant response to history
  conversationHistory.push({
    role: "assistant",
    content: assistantText,
  });

  // Try to parse as JSON
  let parsed;
  try {
    parsed = JSON.parse(assistantText);
  } catch (e) {
    // If not valid JSON, try to extract JSON from markdown code block
    const jsonMatch = assistantText.match(/```(?:json)?\s*\n?([\s\S]*?)\n?```/);
    if (jsonMatch) {
      try {
        parsed = JSON.parse(jsonMatch[1]);
      } catch (e2) {
        parsed = { message: assistantText, data_updates: null };
      }
    } else {
      parsed = { message: assistantText, data_updates: null };
    }
  }

  return parsed;
}

function clearHistory() {
  conversationHistory = [];
}

module.exports = { initClient, isReady, chat, clearHistory };
