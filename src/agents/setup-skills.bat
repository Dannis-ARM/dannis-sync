: npx skills@latest
: skill github - https://github.com/vercel-labs/skills
: sample skills - https://github.com/mattpocock/skills

set HTTPS_PROXY=http://localhost:7890

set mattSkillsGithub=https://github.com/mattpocock/skills
npx skills add %mattSkillsGithub% --list
npx skills add %mattSkillsGithub% --skill tdd -g -a claude-code -y
npx skills add %mattSkillsGithub% --skill grill-with-docs -g -a claude-code -y
npx skills add %mattSkillsGithub% --skill handoff -g -a claude-code -y