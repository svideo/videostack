/**
 * filmed.js 1.4 (10-Aug-2010)
 * (c) by Christian Effenberger 
 * All Rights Reserved
 * Source: filmed.netzgesta.de
 * Distributed under Netzgestade Software License Agreement
 * http://www.netzgesta.de/cvi/LICENSE.txt
 * License permits free of charge
 * use on non-commercial and 
 * private web sites only 
**/

var tmp = navigator.appName == 'Microsoft Internet Explorer' && navigator.userAgent.indexOf('Opera') < 1 ? 1 : 0;
if(tmp) var isIE = document.namespaces && ( !document.documentMode || document.documentMode < 9 ) ? 1 : 0;

if(isIE) {
	if(document.namespaces['v']==null) {
		var e=["shape","shapetype","group","background","path","formulas","handles","fill","stroke","shadow","textbox","textpath","imagedata","line","polyline","curve","roundrect","oval","rect","arc","image"],s=document.createStyleSheet(); 
		for(var i=0; i<e.length; i++) {s.addRule("v\\:"+e[i],"behavior: url(#default#VML);");} document.namespaces.add("v","urn:schemas-microsoft-com:vml");
	} 
}

function getImages(className){
	var children = document.getElementsByTagName('img'); 
	var elements = new Array(); var i = 0;
	var child; var classNames; var j = 0;
	for (i=0;i<children.length;i++) {
		child = children[i];
		classNames = child.className.split(' ');
		for (var j = 0; j < classNames.length; j++) {
			if (classNames[j] == className) {
				elements.push(child);
				break;
			}
		}
	}
	return elements;
}

function getClasses(classes,string){
	var temp = '';
	for (var j=0;j<classes.length;j++) {
		if (classes[j] != string) {
			if (temp) {
				temp += ' '
			}
			temp += classes[j];
		}
	}
	return temp;
}

function getClassValue(classes,string){
	var temp = 0; var pos = string.length;
	for (var j=0;j<classes.length;j++) {
		if (classes[j].indexOf(string) == 0) {
			temp = Math.min(classes[j].substring(pos),100);
			break;
		}
	}
	return Math.max(0,temp);
}

function getClassColor(classes,string){
	var temp = 0; var str = ''; var pos = string.length;
	for (var j=0;j<classes.length;j++) {
		if (classes[j].indexOf(string) == 0) {
			temp = classes[j].substring(pos);
			str = '#' + temp.toLowerCase();
			break;
		}
	}
	if(str.match(/^#[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]$/i)) {
		return str;
	}else {
		return 0;
	}
}

function hex2rgb(val,trans) {
	if(val.length==7) {
		var tp1 = Math.max(0,Math.min(parseInt(val.substr(1,2),16),255));
		var tp2 = Math.max(0,Math.min(parseInt(val.substr(3,2),16),255));
		var tp3 = Math.max(0,Math.min(parseInt(val.substr(5,2),16),255));
		return 'rgba(' + tp1 + ',' + tp2 + ',' + tp3 + ',' + trans + ')';
	}
}

function getClassAttribute(classes,string){
	var temp = 0; var pos = string.length;
	for (var j=0;j<classes.length;j++) {
		if (classes[j].indexOf(string) == 0) {
			temp = 1; break;
		}
	}
	return temp;
}

function roundedRect(ctx,x,y,width,height,radius,nopath){
	if (!nopath) ctx.beginPath();
	ctx.moveTo(x,y+radius);
	ctx.lineTo(x,y+height-radius);
	ctx.quadraticCurveTo(x,y+height,x+radius,y+height);
	ctx.lineTo(x+width-radius,y+height);
	ctx.quadraticCurveTo(x+width,y+height,x+width,y+height-radius);
	ctx.lineTo(x+width,y+radius);
	ctx.quadraticCurveTo(x+width,y,x+width-radius,y);
	ctx.lineTo(x+radius,y);
	ctx.quadraticCurveTo(x,y,x,y+radius);
	if (!nopath) ctx.closePath();
}

function addHoles(ctx,x,y,hw,hh,iw,ih,width,height,dir,tmp) {
	var ww = Math.round(hw/2)-tmp; var wh = Math.round(hh/2)-tmp;
	var ir = Math.max(Math.round(Math.max(ww,wh)/6),1);
	var ow = hw/4; var oh = hh/4; var op = window.opera?1:0;
	if(dir==0) {
		for(var j=0;j<8;j++){
			ctx.save(); roundedRect(ctx,x+ow+(j*hw),y+oh,ww,wh,ir);
			if(op) {ctx.fillStyle='rgba(0,0,0,1)'; ctx.fill();} ctx.clip(); 
			ctx.clearRect(x+ow+(j*hw),y+oh,ww,wh); ctx.restore();
			ctx.save(); roundedRect(ctx,x+ow+(j*hw),y+hh+ih+oh,ww,wh,ir);
			if(op) {ctx.fillStyle='rgba(0,0,0,1)'; ctx.fill();} ctx.clip(); 
			ctx.clearRect(x+ow+(j*hw),y+hh+ih+oh,ww,wh); ctx.restore();
		}	
	}else {
		for(var j=0;j<8;j++){
			ctx.save(); roundedRect(ctx,x+ow,y+oh+(j*hh),ww,wh,ir);
			if(op) {ctx.fillStyle='rgba(0,0,0,1)'; ctx.fill();} ctx.clip(); 
			ctx.clearRect(x+ow,y+oh+(j*hh),ww,wh); ctx.restore();
			ctx.save(); roundedRect(ctx,x+hw+iw+ow,y+oh+(j*hh),ww,wh,ir);
			if(op) {ctx.fillStyle='rgba(0,0,0,1)'; ctx.fill();} ctx.clip(); 
			ctx.clearRect(x+hw+iw+ow,y+oh+(j*hh),ww,wh); ctx.restore();
		}	
	}
}

function addRadialShadow(ctx,x1,y1,r1,x2,y2,r2,o) {
	var tmp = ctx.createRadialGradient(x1,y1,r1,x2,y2,r2);
	tmp.addColorStop(1,'rgba(0,0,0,'+o+')');
	tmp.addColorStop(0,'rgba(0,0,0,0)');
	return tmp;
}

function addLinearShadow(ctx,x,y,w,h,o) {
	var tmp = ctx.createLinearGradient(x,y,w,h);
	tmp.addColorStop(1,'rgba(0,0,0,'+o+')');
	tmp.addColorStop(0,'rgba(0,0,0,0)');
	return tmp;
}

function addHoleShadow(ctx,x,y,w,h,r,o,s) {
	var style; var os = r/2; 
	ctx.beginPath(); ctx.moveTo(x,y+r); ctx.lineTo(x,y+h-r); ctx.quadraticCurveTo(x,y+h,x+r,y+h);
	if(s==0) {ctx.lineTo(x+r,y+(r*2)); ctx.quadraticCurveTo(x+r,y+r,x+(r*2),y+r); ctx.lineTo(x+w,y+r);}
	else {ctx.lineTo(x+r,y+r); ctx.lineTo(x+w,y+r);}
	ctx.quadraticCurveTo(x+w,y,x+w-r,y); ctx.lineTo(x+r,y); ctx.quadraticCurveTo(x,y,x,y+r);
	ctx.fillStyle = 'rgba(0,0,0,'+(o*0.95)+')'; ctx.fill();
	if(s) {
		ctx.beginPath(); ctx.rect(x+(r*2),y+r,w-(r*2),r); ctx.closePath();
		style = addLinearShadow(ctx,x+(r*2),y+(r*2),x+(r*2),y+r,o);
		ctx.fillStyle = style; ctx.fill();
		ctx.beginPath(); ctx.rect(x+r,y+r,r,r); ctx.closePath();
		style = addRadialShadow(ctx,x+(r*2),y+(r*2),0,x+(r*2),y+(r*2),r,o);
		ctx.fillStyle = style; ctx.fill();
		ctx.beginPath(); ctx.rect(x+r,y+(r*2),r,h-(r*2)); ctx.closePath();
		style = addLinearShadow(ctx,x+(r*2),y+(r*2),x+r,y+(r*2),o);
		ctx.fillStyle = style; ctx.fill();
	}
}

function addHoleShadows(ctx,x,y,hw,hh,iw,ih,dir,opac,shadow) {
	var ww = Math.round(hw/2); var wh = Math.round(hh/2);
	var ir = Math.max(Math.round(Math.max(ww,wh)/6),1);
	var ow = hw/4; var oh = hh/4;
	if(dir==0) {
		for(var j=0;j<8;j++) {
			addHoleShadow(ctx,x+ow+(j*hw),y+oh,ww,wh,ir,opac,shadow);
			addHoleShadow(ctx,x+ow+(j*hw),y+hh+ih+oh,ww,wh,ir,opac,shadow);
		}	
	}else {
		for(var j=0;j<8;j++) {
			addHoleShadow(ctx,x+ow,y+oh+(j*hh),ww,wh,ir,opac,shadow);
			addHoleShadow(ctx,x+hw+iw+ow,y+oh+(j*hh),ww,wh,ir,opac,shadow);
		}	
	}
}

function addStripLight(ctx,x,y,width,height,shine) {
	var style = ctx.createLinearGradient(x,y,width,height);
	style.addColorStop(0,'rgba(254,254,254,'+shine+')');
	style.addColorStop(0.1,'rgba(254,254,254,0)');
	style.addColorStop(0.15,'rgba(254,254,254,0)');
	style.addColorStop(0.25,'rgba(254,254,254,'+shine+')');
	style.addColorStop(0.35,'rgba(254,254,254,0)');
	style.addColorStop(0.4,'rgba(254,254,254,0)');
	style.addColorStop(0.5,'rgba(254,254,254,'+shine+')');
	style.addColorStop(0.6,'rgba(254,254,254,0)');
	style.addColorStop(0.65,'rgba(254,254,254,0)');
	style.addColorStop(0.75,'rgba(254,254,254,'+shine+')');
	style.addColorStop(0.85,'rgba(254,254,254,0)');
	style.addColorStop(0.9,'rgba(254,254,254,0)');
	style.addColorStop(1,'rgba(254,254,254,'+shine+')');
	ctx.fillStyle = style;
	ctx.beginPath();
	ctx.rect(x,y,width,height);
	ctx.closePath();
	ctx.fill();
}

function addStripShadow(ctx,x,y,w,h,wd,opac) {
	var style; wd = Math.max(wd,1);
	ctx.fillStyle = 'rgba(0,0,0,'+(opac*0.75)+')'; ctx.fillRect(x,y,w,h);
	style = ctx.createLinearGradient(x,y,x,y-wd); style.addColorStop(0,'rgba(0,0,0,'+opac+')'); style.addColorStop(1,'rgba(0,0,0,0)');
	ctx.beginPath(); ctx.moveTo(x,y); ctx.lineTo(x-wd,y-wd); ctx.lineTo(x+w+wd,y-wd); ctx.lineTo(x+w,y); ctx.closePath();
	ctx.fillStyle = style; ctx.fill();
	style = ctx.createLinearGradient(x,y,x-wd,y); style.addColorStop(0,'rgba(0,0,0,'+opac+')'); style.addColorStop(1,'rgba(0,0,0,0)');
	ctx.beginPath(); ctx.moveTo(x,y); ctx.lineTo(x-wd,y-wd); ctx.lineTo(x-wd,y+h+wd); ctx.lineTo(x,y+h); ctx.closePath();
	ctx.fillStyle = style; ctx.fill();
	style = ctx.createLinearGradient(x,y+h,x,y+h+wd); style.addColorStop(0,'rgba(0,0,0,'+opac+')'); style.addColorStop(1,'rgba(0,0,0,0)');
	ctx.beginPath(); ctx.moveTo(x,y+h); ctx.lineTo(x-wd,y+h+wd); ctx.lineTo(x+w+wd,y+h+wd); ctx.lineTo(x+w,y+h); ctx.closePath();
	ctx.fillStyle = style; ctx.fill();
	style = ctx.createLinearGradient(x+w,y,x+w+wd,y); style.addColorStop(0,'rgba(0,0,0,'+opac+')'); style.addColorStop(1,'rgba(0,0,0,0)');
	ctx.beginPath(); ctx.moveTo(x+w,y+h); ctx.lineTo(x+w+wd,y+h+wd); ctx.lineTo(x+w+wd,y-wd); ctx.lineTo(x+w,y); ctx.closePath();
	ctx.fillStyle = style; ctx.fill();
}

function addIEStrips() {
	var theimages = getImages('filmed');
	var image; var object; var vml; var context; var i;
	var noshadow = 0; var istrip = null; var ishine = null;
	var icolor = ''; var classes = ''; var newClasses = ''; 
	var ishadow = 0; var size = 0; var factor = 0.025; var dir;
	var width = 0; var height = 0; var inset = 0; var color;
	var offset = 0; var ratio = 0.66666667; var softshadow = 0;
	var xoff = 0; var yoff = 0; var whf = 1; var ff = 1;
	var iw = 0; var ih = 0; var ix = 0; var iy = 0; var display = null;
	var hw = 0; var hh = 0; var style = '';	var j = 0; var flt;
	var head; var foot; var fill; var shadow;
	for(i=0;i<theimages.length;i++) {	
		image = theimages[i]; object = image.parentNode; 
		head = ''; foot = ''; fill = ''; shadow = '';
		if(image.width>=80 || image.height>=80) {
			classes = image.className.split(' '); 
			ishine = 0.25; ishadow = 0.33; istrip = 1.0; 
			noshadow = 0; softshadow = 0; 
			size = Math.max(image.width,image.height);
			ishine = getClassValue(classes,"ishine");
			istrip = getClassValue(classes,"istrip");
			ishadow = getClassValue(classes,"ishadow");
			icolor = getClassColor(classes,"icolor");
			noshadow = getClassAttribute(classes,"noshadow");
			softshadow = getClassAttribute(classes,"softshadow");
			newClasses = getClasses(classes,"filmed");
			istrip = istrip==0?1.0:istrip/100;
			ishine = Math.min(ishine==0?0.25:ishine/100,istrip);
			ishadow = Math.min(ishadow==0?33:ishadow,istrip*100);
			color = icolor!=0?icolor:'#000000';
			if(noshadow<1) {offset = Math.max(Math.round(size*factor),1); }else {offset = 0; }
			inset = Math.max(Math.round(offset/2),1);
			if(image.width>=image.height) {
				width = size-offset-(2*inset);
				height = Math.round(width*ratio); dir = 0; 
				yoff = inset+((width-height)*0.5);
				xoff = inset; hw = (size-offset)/8;
				hh = yoff; ff = image.height/image.width;
				if(ff>=ratio) {
					whf = height/image.height;
					ih = height; iy = yoff; 
					iw = Math.round(image.width*whf);
					ix = xoff+((width-iw)*0.5);
				}else {
					whf = width/image.width;
					iw = width; ix = xoff;
					ih = Math.round(image.height*whf);
					iy = yoff+((height-ih)*0.5); 
				}
			}else {
				height = size-offset-(2*inset);
				width = Math.round(height*ratio); dir = 90;
				xoff = inset+((height-width)*0.5);
				yoff = inset; hh = (size-offset)/8;
				hw = xoff; ff = image.width/image.height;
				if(ff>=ratio) {
					whf = width/image.width;
					iw = width; ix = xoff;
					ih = Math.round(image.height*whf);
					iy = yoff+((height-ih)*0.5); 
				}else {
					whf = height/image.height;
					ih = height; iy = yoff; 
					iw = Math.round(image.width*whf);
					ix = xoff+((width-iw)*0.5);
				}
			}
			display = (image.currentStyle.display.toLowerCase()=='block')?'block':'inline-block';        
			vml = document.createElement(['<var style="zoom:1;overflow:hidden;display:' + display + ';width:' + size + 'px;height:' + size + 'px;padding:0;">'].join(''));
			flt = image.currentStyle.styleFloat.toLowerCase();
			display = (flt=='left'||flt=='right')?'inline':display;
			head = '<v:group style="zoom:1; display:' + display + '; margin:-1px 0 0 -1px; padding:0; position:relative; width:' + size + 'px;height:' + size + 'px;" coordsize="' + size + ',' + size + '"><v:rect strokeweight="0" filled="t" stroked="f" fillcolor="#ffffff" style="zoom:1;margin:-1px 0 0 -1px;padding: 0;display:block;position:absolute;top:0px;left:0px;width:' + size + 'px;height:' + size + 'px;"><v:fill color="#ffffff" opacity="0.0" /></v:rect>';
			if(noshadow<1) shadow = '<v:shape strokeweight="0" filled="t" stroked="f" fillcolor="#000000" coordorigin="0,0" coordsize="800,800" path="m 0,0 l 800,0,800,66,775,66,775,45 qy 762,33 l 737,33 qx 725,45 l 725,66,675,66,675,45 qy 662,33 l 637,33 qx 625,45 l 625,66,575,66,575,45 qy 562,33 l 537,33 qx 525,45 l 525,66,475,66,475,45 qy 462,33 l 437,33 qx 425,45 l 425,66,375,66,375,45 qy 362,33 l 337,33 qx 325,45 l 325,66,275,66,275,45 qy 262,33 l 237,33 qx 225,45 l 225,66,175,66,175,45 qy 162,33 l 137,33 qx 125,45 l 125,66,75,66,75,45 qy 62,33 l 37,33 qx 25,45 l 25,88 qy 37,100 l 63,100 qx 75,88 l 75,66,125,66,125,88 qy 137,100 l 163,100 qx 175,88 l 175,66,225,66,225,88 qy 237,100 l 263,100 qx 275,88 l 275,66,325,66,325,88 qy 337,100 l 363,100 qx 375,88 l 375,66,425,66,425,88 qy 437,100 l 463,100 qx 475,88 l 475,66,525,66,525,88 qy 537,100 l 563,100 qx 575,88 l 575,66,625,66,625,88 qy 637,100 l 663,100 qx 675,88 l 675,66,725,66,725,88 qy 737,100 l 763,100 qx 775,88 l 775,66,800,66,800,733,775,733,775,712 qy 762,700 l 737,700 qx 725,712 l 725,733,675,733,675,712 qy 662,700 l 637,700 qx 625,712 l 625,733,575,733,575,712 qy 562,700 l 537,700 qx 525,712 l 525,733,475,733,475,712 qy 462,700 l 437,700 qx 425,712 l 425,733,375,733,375,712 qy 362,700 l 337,700 qx 325,712 l 325,733,275,733,275,712 qy 262,700 l 237,700 qx 225,712 l 225,733,175,733,175,712 qy 162,700 l 137,700 qx 125,712 l 125,733,75,733,75,712 qy 62,700 l 37,700 qx 25,712 l 25,755 qy 37,767 l 63,767 qx 75,755 l 75,733,125,733,125,755 qy 137,767 l 163,767 qx 175,755 l 175,733, 225,733,225,755 qy 237,767 l 263,767 qx 275,755 l 275,733,325,733,325,755 qy 337,767 l 363,767 qx 375,755 l 375,733,425,733,425,755 qy 437,767 l 463,767 qx 475,755 l 475,733,525,733,525,755 qy 537,767 l 563,767 qx 575,755 l 575,733,625,733,625,755 qy 637,767 l 663,767 qx 675,755 l 675,733,725,733,725,755 qy 737,767 l 763,767 qx 775,755 l 775,733,800,733,800,800,0,800 x e" style="filter:Alpha(opacity=' + ishadow + '), progid:dxImageTransform.Microsoft.Blur(PixelRadius=' + inset + ', MakeShadow=false); zoom:1;margin:-1px 0 0 -1px;padding: 0;display:block;position:absolute;top:' + inset + 'px;left:' + inset + 'px;width:' + (size-offset-inset) + 'px;height:' + (size-offset-inset) + 'px; rotation:' + dir + ';"><v:fill color="#000000" opacity="1" /></v:shape>'; 
			fill = '<v:shape strokeweight="0" filled="t" stroked="f" fillcolor="' + color + '" coordorigin="0,0" coordsize="800,800" path="m 0,0 l 800,0,800,66,775,66,775,45 qy 762,33 l 737,33 qx 725,45 l 725,66,675,66,675,45 qy 662,33 l 637,33 qx 625,45 l 625,66,575,66,575,45 qy 562,33 l 537,33 qx 525,45 l 525,66,475,66,475,45 qy 462,33 l 437,33 qx 425,45 l 425,66,375,66,375,45 qy 362,33 l 337,33 qx 325,45 l 325,66,275,66,275,45 qy 262,33 l 237,33 qx 225,45 l 225,66,175,66,175,45 qy 162,33 l 137,33 qx 125,45 l 125,66,75,66,75,45 qy 62,33 l 37,33 qx 25,45 l 25,88 qy 37,100 l 63,100 qx 75,88 l 75,66,125,66,125,88 qy 137,100 l 163,100 qx 175,88 l 175,66,225,66,225,88 qy 237,100 l 263,100 qx 275,88 l 275,66,325,66,325,88 qy 337,100 l 363,100 qx 375,88 l 375,66,425,66,425,88 qy 437,100 l 463,100 qx 475,88 l 475,66,525,66,525,88 qy 537,100 l 563,100 qx 575,88 l 575,66,625,66,625,88 qy 637,100 l 663,100 qx 675,88 l 675,66,725,66,725,88 qy 737,100 l 763,100 qx 775,88 l 775,66,800,66,800,733,775,733,775,712 qy 762,700 l 737,700 qx 725,712 l 725,733,675,733,675,712 qy 662,700 l 637,700 qx 625,712 l 625,733,575,733,575,712 qy 562,700 l 537,700 qx 525,712 l 525,733,475,733,475,712 qy 462,700 l 437,700 qx 425,712 l 425,733,375,733,375,712 qy 362,700 l 337,700 qx 325,712 l 325,733,275,733,275,712 qy 262,700 l 237,700 qx 225,712 l 225,733,175,733,175,712 qy 162,700 l 137,700 qx 125,712 l 125,733,75,733,75,712 qy 62,700 l 37,700 qx 25,712 l 25,755 qy 37,767 l 63,767 qx 75,755 l 75,733,125,733,125,755 qy 137,767 l 163,767 qx 175,755 l 175,733, 225,733,225,755 qy 237,767 l 263,767 qx 275,755 l 275,733,325,733,325,755 qy 337,767 l 363,767 qx 375,755 l 375,733,425,733,425,755 qy 437,767 l 463,767 qx 475,755 l 475,733,525,733,525,755 qy 537,767 l 563,767 qx 575,755 l 575,733,625,733,625,755 qy 637,767 l 663,767 qx 675,755 l 675,733,725,733,725,755 qy 737,767 l 763,767 qx 775,755 l 775,733,800,733,800,800,0,800 x e" style="zoom:1;margin:-1px 0 0 -1px;padding: 0;display:block;position:absolute;top:0px;left:0px;width:' + (size-offset) + 'px;height:' + (size-offset) + 'px; rotation:' + dir + ';"><v:fill method="linear" color="' + color + '" opacity="' + istrip + '" /></v:shape>'; 
			foot = '<v:rect strokeweight="0" filled="t" stroked="f" fillcolor="#000000" style="zoom:1;margin:-1px 0 0 -1px;padding: 0;display:block;position:absolute;top:' + iy + 'px;left:' + ix + 'px;width:' + iw + 'px;height:' + ih + 'px;"><v:fill src="' + image.src + '" type="frame" /></v:rect></v:group>';
			vml.innerHTML = head + shadow + fill + foot;
			vml.className = newClasses;
			vml.style.cssText = image.style.cssText;
			vml.style.visibility = 'visible';
			vml.src = image.src; vml.alt = image.alt;
			vml.width = size; vml.height = size;
			if(image.id!='') vml.id = image.id;
			if(image.title!='') vml.title = image.title;
			if(image.getAttribute('onclick')!='') vml.setAttribute('onclick',image.getAttribute('onclick'));
			object.replaceChild(vml,image);
		}
	}
}

function addStrips() {
	var theimages = getImages('filmed');
	var image; var object; var canvas; var context; var i;
	var noshadow = 0; var istrip = null; var ishine = null;
	var icolor = ''; var classes = ''; var newClasses = ''; 
	var ishadow = 0; var size = 0; var factor = 0.025; var dir;
	var width = 0; var height = 0; var inset = 0; var color;
	var offset = 0; var ratio = 0.66666667; var softshadow = 0;
	var xoff = 0; var yoff = 0; var whf = 1; var ff = 1;
	var iw = 0; var ih = 0; var ix = 0; var iy = 0; 
	var hw = 0; var hh = 0; var style = '';	var j = 0;
	for(i=0;i<theimages.length;i++) {	
		image = theimages[i]; object = image.parentNode; 
		canvas = document.createElement('canvas');
		if(canvas.getContext && (image.width>=80 || image.height>=80)) {
			classes = image.className.split(' '); 
			ishine = 0.25; ishadow = 0.33; istrip = 1.0; 
			noshadow = 0; softshadow = 0; 
			size = Math.max(image.width,image.height);
			ishine = getClassValue(classes,"ishine");
			istrip = getClassValue(classes,"istrip");
			ishadow = getClassValue(classes,"ishadow");
			icolor = getClassColor(classes,"icolor");
			noshadow = getClassAttribute(classes,"noshadow");
			softshadow = getClassAttribute(classes,"softshadow");
			newClasses = getClasses(classes,"filmed");
			canvas.className = newClasses;
			canvas.style.cssText = image.style.cssText;
			canvas.style.height = size+'px';
			canvas.style.width = size+'px';
			canvas.height = size; canvas.width = size;
			canvas.src = image.src; canvas.alt = image.alt;
			if(image.id!='') canvas.id = image.id;
			if(image.title!='') canvas.title = image.title;
			if(image.getAttribute('onclick')!='') canvas.setAttribute('onclick',image.getAttribute('onclick'));
			istrip = istrip==0?1.0:istrip/100;
			ishine = Math.min(ishine==0?0.25:ishine/100,istrip);
			ishadow = Math.min(ishadow==0?0.33:ishadow/100,istrip);
			color = icolor!=0?icolor:'#000000';
			if(noshadow<1) {offset = Math.max(Math.round(size*factor),1); }else {offset = 0; }
			inset = Math.max(Math.round(offset/2),1);
			if(image.width>=image.height) {
				width = canvas.width-offset-(2*inset);
				height = Math.round(width*ratio); dir = 0; 
				yoff = inset+((width-height)*0.5);
				xoff = inset; hw = (canvas.width-offset)/8;
				hh = yoff; ff = image.height/image.width;
				if(ff>=ratio) {
					whf = height/image.height;
					ih = height; iy = yoff; 
					iw = Math.round(image.width*whf);
					ix = xoff+((width-iw)*0.5);
				}else {
					whf = width/image.width;
					iw = width; ix = xoff;
					ih = Math.round(image.height*whf);
					iy = yoff+((height-ih)*0.5); 
				}
			}else {
				height = canvas.height-offset-(2*inset);
				width = Math.round(height*ratio); dir = 1;
				xoff = inset+((height-width)*0.5);
				yoff = inset; hh = (canvas.height-offset)/8;
				hw = xoff; ff = image.width/image.height;
				if(ff>=ratio) {
					whf = width/image.width;
					iw = width; ix = xoff;
					ih = Math.round(image.height*whf);
					iy = yoff+((height-ih)*0.5); 
				}else {
					whf = height/image.height;
					ih = height; iy = yoff; 
					iw = Math.round(image.width*whf);
					ix = xoff+((width-iw)*0.5);
				}
			}
			context = canvas.getContext("2d");
			object.replaceChild(canvas,image);
			context.clearRect(0,0,canvas.width,canvas.height);
			if(noshadow<1) addStripShadow(context,offset*2,offset*2,canvas.width-(3*offset),canvas.height-(3*offset),offset,ishadow);
			context.fillStyle = hex2rgb(color,istrip); 
			context.fillRect(0,0,canvas.width-offset,canvas.height-offset);
			addStripLight(context,0,0,canvas.width-offset,canvas.height-offset,ishine);			
			context.save(); 
			if(window.opera) {context.globalCompositeOperation = "destination-out";}
			addHoles(context,0,0,hw,hh,width,height,canvas.width,canvas.height,dir,0);
			context.restore();
			if(noshadow<1) addHoleShadows(context,0,0,hw,hh,width,height,dir,ishadow,softshadow);
			context.drawImage(image,ix,iy,iw,ih);
			canvas.style.visibility = 'visible';
		}
	}
}

if(window.addEventListener) window.addEventListener("load",addStrips,false);
else window.attachEvent("onload",addIEStrips);