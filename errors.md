$env:API_KEY="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"; aider --model openrouter/google/gemini-2.5-pro-preview

$env:OPENAI_API_KEY="sk-os6REk1CtTQK3HPi0vygHE9GB90QQAoBASpyFO773WGGROTC"; aider --model anthropic/claude-3-7-sonnet:free --base-url https://api.braintrust.dev/v1/proxy

$env:OPENAI_API_KEY="sk-os6REk1CtTQK3HPi0vygHE9GB90QQAoBASpyFO773WGGROTC"; $env:LITELLM_API_BASE="https://api.braintrust.dev/v1/proxy"; aider --model anthropic/

$env:ANTHROPIC_API_KEY="sk-os6REk1CtTQK3HPi0vygHE9GB90QQAoBASpyFO773WGGROTC"; $env:LITELLM_API_BASE="https://api.braintrust.dev/v1/proxy"; aider --model anthropic/claude-3-7-sonnet-latest


$headers = @{
    "Authorization" = "Bearer sk-os6REk1CtTQK3HPi0vygHE9GB90QQAoBASpyFO773WGGROTC"
    "Content-Type"  = "application/json"
}

$body = @{
    model = "claude-3-5-sonnet-20240601"
    messages = @(
        @{ role = "user"; content = "Say hello in Swahili" }
    )
    max_tokens = 100
} | ConvertTo-Json -Depth 10

Invoke-WebRequest -Uri "https://api.braintrust.dev/v1/proxy/v1/messages" -Method POST -Headers $headers -Body $body
