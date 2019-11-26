var exports = module.exports = {};

exports.getDomainNameFromUrl = function(url) {
    let urlRegexp = /^.*\.([a-zA-Z0-9_-]+\.[a-zA-Z]+)$/g;
    let parsedUrl = urlRegexp.exec(url);
    return parsedUrl[1];
}

exports.getDomainNameFromLocalGovernment = function(localGovernment) {
    return this.getDomainNameFromUrl(localGovernment.webSite)
}