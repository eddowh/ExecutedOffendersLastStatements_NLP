//	Breadcrumb script by Paul Davis - http://www.kaosweaver.com - Modified by TDCJ.
//
//	Updated: 11/5/14
//	By: Frank Henderson - TDCJ Web Services
//	Comments: In October 2014, an XSS vulnerability was revealed in this script since it displays unfiltered file path info.
//	A regular expression (regex) was created to check for the presence of < or > in the file path string.
//	If found, a default breadcrumb is displayed instead.
//	New Lines: 49-51. Modified lines: 61, 67, 70

var BC = function() {

  function getLoc(c) {
    var d = "", 
	    k = 0;
    if (c > 0) { 
      for (k = 0; k < c; k+=1) { 
	    d = d + "../"; 
	  }
    }
    return d;
  }
  
  function cDirText(txt) {
	var tomatch = /_/g;
	txt = txt.toUpperCase();
	txt = txt.replace(tomatch, " ");
    switch(txt) {
	  case "DR INFO"				: txt = "INFORMATION"; break;
	  case "R ARTICLES"				: txt = "ARTICLES"; break;
	  case "R WORKGROUP"			: txt = "WORKGROUP"; break;
	  case "IMTDCJ"					: txt = "IMAGES OF TDCJ"; break;
	  case "ES"						: txt = "Executive Services"; break;
	  default						: break;
	}
	
	return txt;
  }
  
  this.breadCrumbs = function(base,delStr,defp,nl) { 
  
    var divs = document.getElementsByTagName("div"),  
	    rtdivs = [], 
	    loc = window.location.toString(), 
        subs = loc.substr(loc.indexOf(base)+base.length).split("/"), 
	    x = 0, 
	    i = 0,
		a = (loc.indexOf(defp) === -1) ? 1 : 2,
		bcfinal = '<a href="' + getLoc(subs.length-1) + defp + '">HOME</a> ' + delStr,
		bcfinal_default = '<a href="http://www.tdcj.texas.gov/index.html">HOME</a>',	// default (safe) URL 
		vURL = /[<|>]/,									// regex to check for HTML tags (< or >)
		URL = decodeURIComponent(window.location);		// must decode URI otherwise regex will fail (%3C will pass for < )

	
	for (x = 0; x < divs.length; x += 1) {
	  if (divs[x].className === "return_to_div") {
		rtdivs.push(divs[x]);  
	  }
	}
	
	for (i = 0; i < (subs.length-a); i+=1) { 
      subs[i] = decodeURIComponent(subs[i]); // was enclosed by makeCaps(), changed decodeURI to decodeURIComponent
	  subs[i] = cDirText(subs[i]);
      bcfinal += '<a href="' + getLoc(subs.length-i-2) + defp + '">' + subs[i] + '</a> ' + delStr;
    }	
    
	bcfinal += (nl === 1) ? "<br />" : "";
    bcfinal += (vURL.test(document.title)) ? "" : document.title;			// test added: display title based on regex
		
	for (x = 0; x < rtdivs.length; x += 1) {     
	  rtdivs[x].innerHTML = (vURL.test(URL)) ? bcfinal_default : bcfinal;	// test added: display bc based on regex
	}
	
  };

};

if (document.getElementById && document.createTextNode && document.getElementsByTagName) {
  		var TDCJBC = new BC(), 
		thome = window.location.hostname + "/";  
		TDCJBC.breadCrumbs(thome, " | ", "index.html", 0);
}