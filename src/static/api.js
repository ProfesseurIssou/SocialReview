/**
 * Récupérer la liste des comptes
 * @returns {Array<{id: number, username: string, platform_id: string, url: string}>}
*/
function Account_Get_All(){
    var accounts = [];
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/accounts', false);
    xhr.send();
    console.log(xhr.responseText);
    if (xhr.status == 200) {
        accounts = JSON.parse(xhr.responseText);
    }
    return accounts;
}
/**
 * Créer un nouveau compte
 * @param {number} account_id
 * @param {number} platform_id
 * @param {string} url
 * @returns {boolean}
*/
function Account_Create(account_id, platform_id, url){
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/account/create', false);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({account_id: account_id, platform_id: platform_id, url: url}));
    return xhr.status == 200;
}



/**
 * Récupérer la liste des plateformes
 * @returns {Array<{id: number, name: string, base_url: string}>}
*/
function Platform_Get_All(){
    var platforms = [];
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/platforms', false);
    xhr.send();
    console.log(xhr.responseText);
    if (xhr.status == 200) {
        platforms = JSON.parse(xhr.responseText);
    }
    return platforms;
}



/**
 * Récupérer la liste des reports
 * @returns {Array<{id: number, account_id: number, report_date: string, report_tag_id: number, report_text: string}>}
*/
function Report_Get_All(){
    var reports = [];
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/reports', false);
    xhr.send();
    console.log(xhr.responseText);
    if (xhr.status == 200) {
        reports = JSON.parse(xhr.responseText);
    }
    return reports;
}


/**
 * Récupérer la liste des tags
 * @returns {Array<{id: number, tag_name: string}>}
*/
function Tag_Get_All(){
    var tags = [];
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/tags', false);
    xhr.send();
    console.log(xhr.responseText);
    if (xhr.status == 200) {
        tags = JSON.parse(xhr.responseText);
    }
    return tags;
}


/**
 * Search username
 * @param {string} username
 * @returns {Array<{id: number, name: string, platform: string, url: string}>}
*/
function Account_Search(username){
    var accounts = [];
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/search', false);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({username: username}));
    console.log(xhr.responseText);
    if (xhr.status == 200) {
        accounts = JSON.parse(xhr.responseText);
    }
    return accounts;
}


/**
 * Get score
 * @param {score: number, interpretation: string, reports: Array<{id: number, tag: string, text: string, date: string}>} report_account_id
 * @returns {number}
*/
function Account_Get_Score(report_account_id){
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/score/'+report_account_id, false);
    xhr.send();
    console.log(xhr.responseText);
    if (xhr.status == 200) {
        return JSON.parse(xhr.responseText);
    }
    return null;
}


/**
 * Send report
 * @param {number} account_id
 * @param {number} tag_id
 * @param {string} text
 * @returns {boolean}
*/
function Report_Create(account_id, tag_id, text){
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/report', false);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({account_id: account_id, tag_id: tag_id, text: text}));
    return xhr.status == 200;
}