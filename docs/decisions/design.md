# Design Decisions

This document summarizes key design decisions for New Arrivals Chi, specifically as they relate to feedback received from users.

## Do not retain any user information for migrants

- **Decision**: No information about the end-user will be stored.
- **Reasons**: 1. Given the vulnerability of the target population, we do not want to risk a potential data breach. 2. We want users to feel safe and secure on the site, and not collecting personal information promotes this.
- **Alternatives Considered**: Allowing new migrants to log in so the site could remember their preferences.
- **Impacts**: The experience will not be personalized, but user security and safety are prioritized over potential UX improvements from login functionality. (Note login functionality does exist for Organizations and Admin and we take care to preserve their information)

## Actionable information over edge cases, systemic policy failures

- **Decision**: Focus on providing resources where users can take actionable steps, even if it means not covering every single edge case.
- **Criteria**: 1. Is this a relatively common scenario new migrants face (based on feedback from Community Based Organizations)? 2. Will users be able to take action after accessing the site or will it require them to contact someone else to redirect to another source (the goal is to avoid the latter for the common cases)?
- **Reasons**: Every person's situation is unique, and the site cannot solve systemic policy problems alone. The effort is better spent sharing commonly needed, actionable information.
- **Examples**:
  - Don't get bogged down in edge cases: Provide resources on common legal statuses (TPS, Asylum, Humanitarian Parole, undocumented) and refer to personalized legal support for uncommon cases.
  - Provide actionable steps, not systemic solutions: While undocumented workers cannot legally work, provide information on workers' rights and reporting workplace violations. There are other channels better suited for tackling systems issues.
- **Alternatives Considered**: This is an ongoing discussion throughout the project.
- **Impacts**: Ideally, this allows managing information bloat, supporting straightforward cases, and freeing staff/volunteers to handle complex cases or systemic issues.

## Build Slowly and Scalably

- **Decision**: Focus on three topics in the first version to gather feedback and iterate before expanding.
- **Reasons**: Gives us time to learn the nuance of the domain and the needs of users. The information provided must be accurate, especially for legal advice. It's also crucial that the tool is user-friendly and so they must be included in the process, even if it slows us down a bit.
- **Example**: The legal flow has gone through three prototyping stages with feedback from community partners at each stage during this V1 phase. Revisions will continue based on user testing with migrants into V2.
- **Impacts**: This slows development by heavily involving the community, but it leads to a better and more useful tool.

## Reduce burden of organization information updates through admin/local admin system

- **Decision**: Organization information will be primarily updated by an admin (or group of admins) rather than solely by individual organizations.
- **Reasons**: Individual organizations have limited capacity to keep information up-to-date, and community volunteers already gather this information informally.
- **Alternatives Considered**: The original plan was to give organizations an easy toggle to update their information, but feedback indicated they were unlikely to do so.
- **Impacts**: Ideally, this allows for more regular and reliable updates while reducing the burden on organizations and still giving them autonomy to update their information if desired.

## First, focus on general information about Chicago, Legal Aid, and Health

- **Decision**: The first phase focuses on general Chicago information, legal aid (mostly related to obtaining legal status), and health.
- **Reasons**: These were identified as the most urgent and actionable needs for new migrants, meeting the principle of providing actionable information.
  - General Chicago Information: Requested by partners and includes actionable items like obtaining IDs and enrolling in school.
  - Legal: One of the first things migrants need to do, with time limitations for applying. Obtaining legal status if eligible is also a pre requisite to work
  - Health: New arrivals often face urgent health issues.
- **Alternatives Considered**: Housing and Food were considered for V1 but deferred (Food due to an existing robust tool through Food Depository, Housing due to complexity).
- **Impacts**: This allows V1 to be ready with the most important information, providing templates to build upon for future versions with additional topics.