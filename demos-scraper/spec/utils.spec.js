const Utils = require('../src/utils.js');

describe("getDomainFromUrl", function() {
  
    it("should return metz.fr from http://www.metz.fr", function() {
      expect(Utils.getDomainNameFromUrl('http://www.metz.fr')).toBe('metz.fr');
    });

    it("should return bechy.fr from http://www.bechy.fr", function() {
      expect(Utils.getDomainNameFromUrl('http://www.bechy.fr')).toBe('bechy.fr');
    });

    it("should return bechy.fr from https://www.bechy.fr", function() {
      expect(Utils.getDomainNameFromUrl('https://www.bechy.fr')).toBe('bechy.fr');
    });

    it("should return bechy.fr from www.bechy.fr", function() {
      expect(Utils.getDomainNameFromUrl('www.bechy.fr')).toBe('bechy.fr');
    });

    it("should return bechy-57.fr from www.bechy-57.fr", function() {
      expect(Utils.getDomainNameFromUrl('www.bechy-57.fr')).toBe('bechy-57.fr');
    });

    it("should return bechy-57.org from https://www.mairie.bechy-57.fr", function() {
      expect(Utils.getDomainNameFromUrl('www.mairie.bechy-57.fr')).toBe('bechy-57.fr');
    });

    it("should return '' from null", function() {
      expect(Utils.getDomainNameFromUrl(null)).toBe(null);
    });
  });

  describe("getFullHttpsUrl", function(){
    it("should return http://metz.fr from metz.fr", function() {
      expect(Utils.getUrlWithProtocol('metz.fr')).toBe('http://metz.fr');
    });

    it("should return https://metz.fr from https://metz.fr", function() {
      expect(Utils.getUrlWithProtocol('https://metz.fr')).toBe('https://metz.fr');
    });

    it("should return http://metz.fr from http://metz.fr", function() {
      expect(Utils.getUrlWithProtocol('http://metz.fr')).toBe('http://metz.fr');
    });

    it("should return ftp://metz.fr from ftp://metz.fr", function() {
      expect(Utils.getUrlWithProtocol('ftp://metz.fr')).toBe('ftp://metz.fr');
    });
  });