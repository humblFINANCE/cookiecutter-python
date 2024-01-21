module.exports = {
    messages: {
        type: "Select the TYPE of change that you're committing:",
        scope: "Denote the SCOPE of this change:",
        customScope: "Denote the SCOPE of this change:",
        subject: "Write a SHORT, IMPERATIVE tense description of the change:\n",
        body: 'Provide a LONGER description of the change (optional). Use "|" to break new line:\n',
        breaking: 'List any BREAKING CHANGES (optional). Use "|" to break new line:\n',
        footerPrefixesSelect: "Select the ISSUES type of changeList by this change (optional):",
        customFooterPrefix: "Input ISSUES prefix:",
        footer: "List any ISSUES by this change. E.g.: #31, #34:\n",
        generatingByAI: 'Generating your AI commit subject...',
        generatedSelectByAI: 'Select suitable subject by AI generated:',
        confirmCommit: "Are you sure you want to proceed with the commit above?"
    },
    types: [
        { value: "feat", name: "A new feature" },
        { value: "fix", name: "A bug fix" },
        { value: "hotfix", name: "A temporary hotfix" },
        { value: "chore", name: "Other changes that don't modify src or test files" },
        { value: "refactor", name: "A code change that neither fixes a bug nor adds a feature" },
        { value: "WIP", name: "A code change that is in progress, adding a feature or fix" },
        { value: "docs", name: "Documentation only changes" },
        { value: "perf", name: "A code change that improves performance" },
        { value: "style", name: "Changes that do not affect the meaning of the code" },
        { value: "build", name: "Changes that affect the build system or external dependencies" },
        { value: "ci", name: "Changes to our CI configuration files and scripts" },
        { value: "test", name: "Adding missing tests or correcting existing tests" },
        { value: "revert", name: "Reverts a previous commit" },
        { value: "add_dep", name: "Add a dependency" },
        { value: "rem_dep", name: "Remove a dependency" }
    ],
    usePreparedCommit: false, // to re-use commit from ./.git/COMMIT_EDITMSG
    allowTicketNumber: true,
    isTicketNumberRequired: true,
    ticketNumberPrefix: 'TICKET-',
    ticketNumberRegExp: '\\d{1,5}',
    scopeOverrides: {
        'add_dep': [
            { name: 'conda' },
            { name: 'pip' },
            { name: 'poetry' }
        ]
    },
    allowCustomScopes: true,
    allowBreakingChanges: ['feat', 'fix'],
    subjectLimit: 100,
}