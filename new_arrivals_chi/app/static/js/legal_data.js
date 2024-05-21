/**
 Project: new_arrivals_chi
File name: legal_data.js
Associated Files:
    base.html, main.py, legal_flow.html, legal_flow.js, legal.css

Javascript Objects for the Legal Resource Flow
**/
const options = {
    legal_start: {
        key: "legal",
        header: "what_help",
        children: {
            work_auth: {
                key: "work_auth",
                header: "work_auth_question",
                children: {
                    tps: {
                        key: "tps", header: "tps_header", desc: "tps_desc", children: {
                            option1: { key: "tps_info", link: "/legal/tps_info" },
                            option2: { key: "tps_apply", link: "/legal/tps_apply" }
                        }
                    },
                    vttc: {
                        key: "vttc", header: "vttc_header", desc: "vttc_desc", children: {
                            option1: { key: "vttc_info", link: "/legal/vttc_info" },
                            option2: { key: "vttc_apply", link: "/legal/vttc_apply" }
                        }
                    },
                    asylum: {
                        key: "asylum", header: "asylum_header", desc: "asylum_desc", children: {
                            option1: { key: "asylum_info", link: "/legal/asylum_info" },
                            option2: { key: "asylum_apply", link: "/legal/asylum_apply" }
                        }
                    },
                    parole: {
                        key: "parole", header: "parole_header", desc: "parole_desc", children: {
                            option1: { key: "parole_info", link: "/legal/parole_info" },
                            option2: { key: "parole_apply", link: "/legal/parole_apply" }
                        }
                    },
                    other: {
                        key: "other", header: "other_header", desc: "other_desc", children: {
                            option1: { key: "undocumented", link: "/legal/undocumented_resources" },
                            option2: { key: "lawyers", link: "/legal/lawyers" }
                        }
                    },
                }
            },
            work_rights: { key: "work_rights", link: "/legal/work_rights" },
            renters_rights: { key: "renters_rights", link: "/legal/renters_rights" },
            something_else: { key: "something_else", link: "/legal/lawyers" }
        }
    }
};
