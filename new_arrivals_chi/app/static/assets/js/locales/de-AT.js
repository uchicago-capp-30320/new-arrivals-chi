(function () {
	"use strict";

	if (typeof Date.dp_locales === 'undefined') {
		Date.dp_locales = {
		    "texts": {
		        "buttonTitle": "Zeitraum auswählen ...",
		        "buttonLabel": "Klicken Sie auf oder drücken Sie die Eingabetaste oder die Leertaste, um den Kalender zu öffnen",
		        "prevButtonLabel": "Zum Vormonat",
		        "nextButtonLabel": "Zum nächsten Monat",
		        "closeButtonTitle": "Schließen",
		        "closeButtonLabel": "Schließen Sie die Kalender",
		        "prevMonthButtonLabel": "Zum Vorjahr",
		        "prevYearButtonLabel": "Gehen Sie zu den vorherigen 20 Jahre",
		        "nextMonthButtonLabel": "Zum nächsten Jahr",
		        "nextYearButtonLabel": "Gehen Sie zu den nächsten zwanzig Jahren",
		        "changeMonthButtonLabel": "Klicken Sie auf oder drücken Sie die Eingabetaste oder die Leertaste, um den Monat zu ändern",
		        "changeYearButtonLabel": "Klicken Sie auf oder drücken Sie die Enter-Taste oder das Jahr der Leertaste wechseln",
		        "changeRangeButtonLabel": "Klicken Sie auf oder drücken Sie die Eingabetaste oder die Leertaste, um zu den nächsten zwanzig Jahren gehen",
		        "calendarHelp": "- Pfeil nach oben und Pfeil nach unten - geht auf den gleichen Tag in der Woche in der vorherigen oder nächsten Woche auf. Wenn das Ende des Monats erreicht ist, setzt sich in der vorherigen oder nächsten Monat nach Bedarf.\r\n- Pfeil nach links und Pfeil nach rechts - rückt einem Tag zum nächsten, auch in einem Kontinuum. Visuell Fokus von Tag zu Tag verschoben und wickelt von Reihe zu im Raster von Tagen zu rudern.\r\n- Strg + Page Up - Wechselt zum gleichen Zeitpunkt im Vorjahr.\r\n- Steuerung + Bild ab - Wechselt zum gleichen Zeitpunkt im nächsten Jahr.\r\n- Startseite - Wechselt zum ersten Tag des aktuellen Monats.\r\n- Ende - Moves auf den letzten Tag des laufenden Monats.\r\n- Page Up - Wechselt zum gleichen Zeitpunkt im Vormonat.\r\n- Page Down - Wechselt zum gleichen Zeitpunkt in den nächsten Monat.\r\n- Geben Sie oder Espace - schließt den Kalender, und das ausgewählte Datum wird in das entsprechende Textfeld angezeigt.\r\n- Escape - schließt den Kalender ohne Aktion."
		    },
		    "directionality": "LTR",
		    "month_names": [
		        "Jänner",
		        "Februar",
		        "März",
		        "April",
		        "Mai",
		        "Juni",
		        "Juli",
		        "August",
		        "September",
		        "Oktober",
		        "November",
		        "Dezember"
		    ],
		    "month_names_abbreviated": [
		        "Jän.",
		        "Feb.",
		        "März",
		        "Apr.",
		        "Mai",
		        "Juni",
		        "Juli",
		        "Aug.",
		        "Sep.",
		        "Okt.",
		        "Nov.",
		        "Dez."
		    ],
		    "month_names_narrow": [
		        "J",
		        "F",
		        "M",
		        "A",
		        "M",
		        "J",
		        "J",
		        "A",
		        "S",
		        "O",
		        "N",
		        "D"
		    ],
		    "day_names": [
		        "Sonntag",
		        "Montag",
		        "Dienstag",
		        "Mittwoch",
		        "Donnerstag",
		        "Freitag",
		        "Samstag"
		    ],
		    "day_names_abbreviated": [
		        "So.",
		        "Mo.",
		        "Di.",
		        "Mi.",
		        "Do.",
		        "Fr.",
		        "Sa."
		    ],
		    "day_names_short": [
		        "So.",
		        "Mo.",
		        "Di.",
		        "Mi.",
		        "Do.",
		        "Fr.",
		        "Sa."
		    ],
		    "day_names_narrow": [
		        "S",
		        "M",
		        "D",
		        "M",
		        "D",
		        "F",
		        "S"
		    ],
		    "day_periods": {
		        "afternoon": "nachmittags",
		        "am": "vorm.",
		        "earlyMorning": "morgens",
		        "evening": "abends",
		        "morning": "vormittags",
		        "night": "nachts",
		        "noon": "mittags",
		        "pm": "nachm."
		    },
		    "day_periods_abbreviated": {
		        "afternoon": "nachmittags",
		        "am": "vorm.",
		        "earlyMorning": "morgens",
		        "evening": "abends",
		        "morning": "vormittags",
		        "night": "nachts",
		        "noon": "mittags",
		        "pm": "nachm."
		    },
		    "day_periods_narrow": {
		        "am": "vm.",
		        "noon": "m.",
		        "pm": "nm."
		    },
		    "quarter_names": [
		        "1. Quartal",
		        "2. Quartal",
		        "3. Quartal",
		        "4. Quartal"
		    ],
		    "quarter_names_abbreviated": [
		        "Q1",
		        "Q2",
		        "Q3",
		        "Q4"
		    ],
		    "quarter_names_narrow": [
		        "1",
		        "2",
		        "3",
		        "4"
		    ],
		    "era_names": [
		        "v. Chr.",
		        "n. Chr."
		    ],
		    "era_names_abbreviated": [
		        "v. Chr.",
		        "n. Chr."
		    ],
		    "era_names_narrow": [
		        "v. Chr.",
		        "n. Chr."
		    ],
		    "full_format": "EEEE, d. MMMM y",
		    "long_format": "d. MMMM y",
		    "medium_format": "dd.MM.y",
		    "short_format": "dd.MM.yy",
		    "firstday_of_week": 1
		};
	}
})();