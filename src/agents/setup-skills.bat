: npx skills@latest
: skill github - https://github.com/vercel-labs/skills
: sample skills - https://github.com/mattpocock/skills

set HTTPS_PROXY=http://localhost:7890

set mattSkillsGithub=https://github.com/mattpocock/skills
: npx skills add %mattSkillsGithub% --list
npx skills add %mattSkillsGithub% --skill ^
    tdd ^
    grill-with-docs ^
    handoff ^
    improve-codebase-architecture ^
    diagnose ^
    -g -a claude-code -y