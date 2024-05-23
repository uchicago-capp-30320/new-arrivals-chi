/**
Project: new_arrivals_chi
File name: legal_flow.js
Associated Files:
    base.html, main.py, legal_flow.html, legal_data.js, legal.css

This file contains the JavaScript logic for dynamically generating a decision tree of options on a legal assistance webpage.
The options are presented as buttons, which users can click to navigate through various legal topics and resources.
The page includes functionality for creating buttons, managing navigation, and handling user interactions.
**/

// store previous options for back button
const previousOptions = [];

// create buttons based on the current options based on decision tree level
function createButtons(currentOptions, language, parentColor = '') {
    $('#buttonContainer').empty();

    // get the header text from the language data
    const headerText = getHeaderText(currentOptions);
    $('#buttonContainer').append($('<div>').addClass('box-title').text(headerText));

    // create a group for the buttons at this level
    const buttonGroup = $('<div>').addClass('button-group');

    // create children buttons
    Object.keys(currentOptions.children).forEach(key => {
        const childOption = currentOptions.children[key];
        buttonGroup.append(createChildButton(childOption, key, parentColor, currentOptions, language));
    });

    $('#buttonContainer').append(buttonGroup);

    // add to back button
    if (previousOptions.length > 0) {
        const backBtn = createBackButton(language);
        $('#buttonContainer').append(backBtn);
    }
}

// get header text from language data
function getHeaderText(currentOptions) {
    return currentOptions.header && languageData[currentOptions.header]
        ? languageData[currentOptions.header]
        : 'Select an option';
}

// get button description from language data
function getButtonDescription(childOption) {
    return childOption.desc && languageData[childOption.desc]
        ? languageData[childOption.desc].split('\n').map(item => `<li>${item}</li>`).join('')
        : '';
}

// determine the color class for the button
function getColorClass(key) {
    switch (key) {
        case 'work_auth':
            return 'button-blue';
        case 'work_rights':
            return 'button-yellow';
        case 'renters_rights':
            return 'button-green';
        case 'something_else':
            return 'button-orange';
        default:
            return 'button-blue';
    }
}

// create a button element
function createButton(btnText, colorClass, childOption, currentOptions, language) {
    return $('<button>')
        .addClass('button')
        .addClass(colorClass)
        .text(btnText)
        .on('click', () => {
            if (childOption.children) {
                previousOptions.push(currentOptions);
                createButtons(childOption, language, colorClass);
            } else if (childOption.link) {
                navigateTo(childOption.link, language);
            }
        });
}

// create a child button element
function createChildButton(childOption, key, parentColor, currentOptions, language) {
    const btnText = languageData[childOption.key] || 'Key not found';
    const btnDesc = getButtonDescription(childOption);
    const colorClass = getColorClass(key);
    const btn = createButton(btnText, colorClass, childOption, currentOptions, language);

    const collapsible = $('<div>').addClass('collapsible').html(btnDesc);
    const buttonWrapper = $('<div>').addClass('button-wrapper').append(btn);

    if (btnDesc && btnDesc.trim() !== '') {
        const toggleLink = createToggleLink(collapsible, language);
        buttonWrapper.append(collapsible).append(toggleLink);
    }

    return buttonWrapper;
}

// create a toggle link for collapsible description
function createToggleLink(collapsible, language) {
    return $('<span>')
        .addClass('toggle-link')
        .text(languageData.see_options)
        .on('click', function () {
            collapsible.toggleClass('show');
            $(this).text(collapsible.hasClass('show') ? languageData.hide_options : languageData.see_options);
        });
}

// create a back button element
function createBackButton(language) {
    return $('<button>')
        .addClass('button yellow-button')
        .text('Back')
        .on('click', () => {
            const prevOptions = previousOptions.pop();
            createButtons(prevOptions, language);
        });
}

// navigate to a specific URL with language parameter
function navigateTo(destination, language) {
    const url = new URL(destination, window.location.origin);
    url.searchParams.set('lang', language);
    window.location.href = url.toString();
}

// document ready function
$(document).ready(function() {
    createButtons(options.legal_start, language);
});
