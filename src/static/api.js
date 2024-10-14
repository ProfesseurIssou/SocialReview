////////// USER //////////
/**
Récupération du nombre total d'utilisateur
@returns {Number}
*/
function User_Count_All(){
    var count = 0;
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/user/count/all', false);
    xhr.send();
    console.log(xhr.responseText);
    if (xhr.status == 200) {
        count = JSON.parse(xhr.responseText);
    }
    return Number(count["count"]);
}
/**
Récupération de la liste des utilisateurs
@returns {Array<{id: number, names: Array<string>, platforms: Object<string, TypeURL>}>}
*/
function User_Get_All(){
    var users = [];
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/user/list/all', false);
    xhr.send();
    console.log(xhr.responseText);
    if (xhr.status == 200) {
        users = JSON.parse(xhr.responseText);
    }
    return users["users"];
}

/**
Ajout d'un utilisateur
@param {Array<string>} names ["name1", "name2"]
@returns {Number} ID de l'utilisateur
*/
function User_Add(names){
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/user/add', false);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({
        "names": names
    }));
    console.log(xhr.responseText);
    if (xhr.status == 200) {
        return Number(JSON.parse(xhr.responseText)["id"]);
    }
    return -1;
}
/**
Supprimer un utilisateur
@param {Number} userID userID
@returns {Boolean} True si la suppression s'est bien passé
*/
function User_Delete(userID){
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/user/delete', false);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({
        "userID": userID
    }));
    console.log(xhr.responseText);
    result = JSON.parse(xhr.responseText);
    if ("error" in result){
        return false;
    }
    return true;
}
/**
Mis à jour d'un utilisateur
@param {Number} userID userID
@param {Array<string>} names ["name1", "name2"]
@param {Object<string, Array<string>>} platforms {"platform1": ["url"], "platform2": ["url"]}
@param {Array<Number>} tags [1, 2, 3]
@returns {Boolean} True si la mise à jour s'est bien passé
*/
function User_Update(userID, names, platforms, tags){
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/user/update', false);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({
        "userID": userID,
        "names": names,
        "platforms": platforms,
        "tags": tags
    }));
    result = JSON.parse(xhr.responseText);
    console.log(result);
    if ("error" in result){
        return false;
    }
    return true;
}
//////////////////////////



////////// MEDIA //////////
/**
Récupère le nombre des nouveaux médias d'un utilisateur sur une platform
@param {Number} userID
@param {String} platformName
@returns {Number} Nombre de médias
*/
function Media_Count(userID, platformName){
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/media/count', false);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({
        "userID": userID,
        "platform": platformName
    }));
    console.log(xhr.responseText);
    if (xhr.status == 200) {
        return Number(JSON.parse(xhr.responseText)["count"]);
    }
    return -1;
}
/**
Récupère le nombre des nouveaux médias de tout les utilisateurs sur toutes les platforms
{
    "userID": {
        "deviantart": 1
    },
    "userID2": {
        "deviantart": 1,
        "pixiv": 1
    }
}
@returns {Object<string, Object<string, Number>>}
*/
function Media_Count_All(){
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/media/count/all', false);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send();
    console.log(xhr.responseText);
    if (xhr.status == 200) {
        return JSON.parse(xhr.responseText);
    }
    return {};
}
/**
Télécharge les nouveaux médias d'un utilisateur sur une platform
@param {Number} userID
@param {String} platformName
@returns {Boolean} True si le téléchargement s'est bien passé
*/
function Media_Download(userID, platformName){
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/media/download', false);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({
        "userID": userID,
        "platform": platformName
    }));
    console.log(xhr.responseText);
    if (xhr.status == 200) {
        return true;
    }
    return false;
}
///////////////////////////




////////// PLATFORM //////////
/**
Récupération du nombre total de platform
@returns {Number}
*/
function Platform_Count_All(){
    var count = 0;
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/platform/count/all', false);
    xhr.send();
    console.log(xhr.responseText);
    if (xhr.status == 200) {
        count = JSON.parse(xhr.responseText);
    }
    return Number(count["count"]);
}
/**
Récupération de la liste des plateformes
@returns {Array<string>} Liste des plateformes ["platform1", "platform2"]
*/
function Platform_Get_All(){
    var platforms = [];
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/platform/list/all', false);
    xhr.send();
    console.log(xhr.responseText);
    if (xhr.status == 200) {
        platforms = JSON.parse(xhr.responseText);
    }
    return platforms["platforms"];
}
//////////////////////////////



////////// CONFIG //////////
/**
Récupération de la configuration
@returns {Object<string, string>} {"key": "value"}
*/
function Config_Get(){
    var config = {};
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/config/get', false);
    xhr.send();
    console.log(xhr.responseText);
    if (xhr.status == 200) {
        config = JSON.parse(xhr.responseText);
    }
    return config;
}
/**
Mis à jour de la configuration
@param {Object<string, string>} config {"key": "value"}
@returns {Boolean} True si la mise à jour s'est bien passé
*/
function Config_Update(config){
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/config/update', false);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify(config));
    console.log(xhr.responseText);
    result = JSON.parse(xhr.responseText);
    if ("error" in result){
        return false;
    }
    return true;
}
////////////////////////////


////////// COOKIES //////////
/**
Récupération des cookies
@returns {Object<string, string>} {"key": "value"}
*/
function Cookies_Get(){
    var cookies = {};
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/cookies/get', false);
    xhr.send();
    console.log(xhr.responseText);
    if (xhr.status == 200) {
        cookies = JSON.parse(xhr.responseText);
    }
    return cookies;
}
/**
Mis à jour des cookies
@param {Object<string, Array<Object>>} cookies {"key": "value"}
@returns {Boolean} True si la mise à jour s'est bien passé
*/
function Cookies_Update(cookies){
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/cookies/update', false);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify(cookies));
    console.log(xhr.responseText);
    result = JSON.parse(xhr.responseText);
    if ("error" in result){
        return false;
    }
    return true;
}
/**
Test des cookies
@returns {Object<string, Boolean>} True si les cookies sont valides
*/
function Cookies_Test(){
    var cookies = {};
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/cookies/test', false);
    xhr.send();
    console.log(xhr.responseText);
    if (xhr.status == 200) {
        cookies = JSON.parse(xhr.responseText);
    }
    return cookies;
}
/////////////////////////////



////////// TAGS //////////
/**
Récupération du nombre total de tags
@returns {Number}
*/
function Tag_Count_All(){
    var count = 0;
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/tags/count', false);
    xhr.send();
    console.log(xhr.responseText);
    if (xhr.status == 200) {
        count = JSON.parse(xhr.responseText);
    }
    return Number(count["count"]);
}
/**
Récupération de la liste des tags
@returns {Object<string, string>}
*/
function Tag_Get_All(){
    var tags = {};
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/tags/list/all', false);
    xhr.send();
    console.log(xhr.responseText);
    if (xhr.status == 200) {
        tags = JSON.parse(xhr.responseText);
    }
    return tags;
}
/**
Ajout d'un tag
@param {String} tag
@returns {Boolean} True si l'ajout s'est bien passé
*/
function Tag_Add(tag){
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/tags/add', false);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({
        "name": tag
    }));
    console.log(xhr.responseText);
    result = JSON.parse(xhr.responseText);
    if ("error" in result){
        return false;
    }
    return true;
}
/**
Supprimer un tag
@param {Number} tagID
@returns {Boolean} True si la suppression s'est bien passé
*/
function Tag_Delete(tagID){
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/tags/delete', false);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({
        "tagID": tagID
    }));
    console.log(xhr.responseText);
    result = JSON.parse(xhr.responseText);
    if ("error" in result){
        return false;
    }
    return true;
}
//////////////////////////