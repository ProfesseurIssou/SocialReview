////////// ACCOUNT //////////
/**
 * Récupérer la liste des comptes
 * @returns {Array<{id: number, name: string, platform: string, url: string}>}
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
/////////////////////////////



