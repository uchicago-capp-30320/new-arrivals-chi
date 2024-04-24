# Frontend Framework Decisions

This document summarizes key frontend decisions in New Arrivals Chi.

## Technology Decision

- **Decision**: We decided to use *Flask* as our front-end technology. The languages used to build our webpages are HTML to markup the webpage, CSS for special styling, Jinja2 (Python) for the template engine, and JavaScript for simple functions.

- **Reasons**: As our website will not be feature-rich--incorporating only three primary features (login, search, and static pages)--we opted to use Flask as it is a lightweight framework that has a lower barrier to entry.

- **Alternatives Considered**: *Django*: as the sole alternative considered, we opted for Flask instead due the aforementioned reasons.

- **Impacts**: If we decided we wanted a feature-rich application in the future, there could be a potential downside in scaling up to add many unique features. However, we do not anticipate this to be an issue in the future.
