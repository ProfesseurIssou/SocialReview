/**
 * Récupérer la liste des comptes
 * @returns {Array<{id: number, username: string, platform: string, url: string}>}
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
 * Récupérer la liste des repports
 * @returns {Array<{id: number, account_id: number, repport_date: string, repport_tag_id: number, repport_text: string}>}
*/
function Repport_Get_All(){
    var repports = [];
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/repports', false);
    xhr.send();
    console.log(xhr.responseText);
    if (xhr.status == 200) {
        repports = JSON.parse(xhr.responseText);
    }
    return repports;
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


