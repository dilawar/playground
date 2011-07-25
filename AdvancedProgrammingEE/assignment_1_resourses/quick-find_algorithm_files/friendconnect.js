window.google = window["google"] || {};google.friendconnect = google.friendconnect_ || {};if (!window['__ps_loaded__']) {/*http://www.a.friendconnect.gmodules.com/gadgets/js/rpc.js?c=1*/
var gadgets=gadgets||{},shindig=shindig||{},osapi=osapi||{};
;
gadgets.config=function(){var A=[];
var B;
return{register:function(E,D,C){var F=A[E];
if(!F){F=[];
A[E]=F
}F.push({validators:D||{},callback:C})
},get:function(C){if(C){return B[C]||{}
}return B
},init:function(E,L){B=E;
for(var C in A){if(A.hasOwnProperty(C)){var D=A[C],I=E[C];
for(var H=0,G=D.length;
H<G;
++H){var J=D[H];
if(I&&!L){var F=J.validators;
for(var K in F){if(F.hasOwnProperty(K)){if(!F[K](I[K])){throw new Error('Invalid config value "'+I[K]+'" for parameter "'+K+'" in component "'+C+'"')
}}}}if(J.callback){J.callback(E)
}}}}},EnumValidator:function(F){var E=[];
if(arguments.length>1){for(var D=0,C;
(C=arguments[D]);
++D){E.push(C)
}}else{E=F
}return function(H){for(var G=0,I;
(I=E[G]);
++G){if(H===E[G]){return true
}}}
},RegExValidator:function(C){return function(D){return C.test(D)
}
},ExistsValidator:function(C){return typeof C!=="undefined"
},NonEmptyStringValidator:function(C){return typeof C==="string"&&C.length>0
},BooleanValidator:function(C){return typeof C==="boolean"
},LikeValidator:function(C){return function(E){for(var F in C){if(C.hasOwnProperty(F)){var D=C[F];
if(!D(E[F])){return false
}}}return true
}
}}
}();;
gadgets.log=(function(){var E=1;
var A=2;
var F=3;
var C=4;
var D=function(I){B(E,I)
};
gadgets.warn=function(I){B(A,I)
};
gadgets.error=function(I){B(F,I)
};
gadgets.setLogLevel=function(I){H=I
};
function B(J,I){if(J<H||!G){return 
}if(J===A&&G.warn){G.warn(I)
}else{if(J===F&&G.error){G.error(I)
}else{if(G.log){G.log(I)
}}}}D.INFO=E;
D.WARNING=A;
D.NONE=C;
var H=E;
var G=window.console?window.console:window.opera?window.opera.postError:undefined;
return D
})();;
var tamings___=tamings___||[];
tamings___.push(function(A){___.grantRead(gadgets.log,"INFO");
___.grantRead(gadgets.log,"WARNING");
___.grantRead(gadgets.log,"ERROR");
___.grantRead(gadgets.log,"NONE");
caja___.whitelistFuncs([[gadgets,"log"],[gadgets,"warn"],[gadgets,"error"],[gadgets,"setLogLevel"]])
});;
if(window.JSON&&window.JSON.parse&&window.JSON.stringify){gadgets.json=(function(){var A=/___$/;
return{parse:function(C){try{return window.JSON.parse(C)
}catch(B){return false
}},stringify:function(C){try{return window.JSON.stringify(C,function(E,D){return !A.test(E)?D:null
})
}catch(B){return null
}}}
})()
}else{gadgets.json=function(){function f(n){return n<10?"0"+n:n
}Date.prototype.toJSON=function(){return[this.getUTCFullYear(),"-",f(this.getUTCMonth()+1),"-",f(this.getUTCDate()),"T",f(this.getUTCHours()),":",f(this.getUTCMinutes()),":",f(this.getUTCSeconds()),"Z"].join("")
};
var m={"\b":"\\b","\t":"\\t","\n":"\\n","\f":"\\f","\r":"\\r",'"':'\\"',"\\":"\\\\"};
function stringify(value){var a,i,k,l,r=/["\\\x00-\x1f\x7f-\x9f]/g,v;
switch(typeof value){case"string":return r.test(value)?'"'+value.replace(r,function(a){var c=m[a];
if(c){return c
}c=a.charCodeAt();
return"\\u00"+Math.floor(c/16).toString(16)+(c%16).toString(16)
})+'"':'"'+value+'"';
case"number":return isFinite(value)?String(value):"null";
case"boolean":case"null":return String(value);
case"object":if(!value){return"null"
}a=[];
if(typeof value.length==="number"&&!value.propertyIsEnumerable("length")){l=value.length;
for(i=0;
i<l;
i+=1){a.push(stringify(value[i])||"null")
}return"["+a.join(",")+"]"
}for(k in value){if(k.match("___$")){continue
}if(value.hasOwnProperty(k)){if(typeof k==="string"){v=stringify(value[k]);
if(v){a.push(stringify(k)+":"+v)
}}}}return"{"+a.join(",")+"}"
}}return{stringify:stringify,parse:function(text){if(/^[\],:{}\s]*$/.test(text.replace(/\\["\\\/b-u]/g,"@").replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g,"]").replace(/(?:^|:|,)(?:\s*\[)+/g,""))){return eval("("+text+")")
}return false
}}
}()
}gadgets.json.flatten=function(C){var D={};
if(C===null||C===undefined){return D
}for(var A in C){if(C.hasOwnProperty(A)){var B=C[A];
if(null===B||undefined===B){continue
}D[A]=(typeof B==="string")?B:gadgets.json.stringify(B)
}}return D
};;
var tamings___=tamings___||[];
tamings___.push(function(A){___.tamesTo(gadgets.json.stringify,safeJSON.stringify);
___.tamesTo(gadgets.json.parse,safeJSON.parse)
});;
gadgets.util=function(){function G(K){var L;
var I=K.indexOf("?");
var J=K.indexOf("#");
if(J===-1){L=K.substr(I+1)
}else{L=[K.substr(I+1,J-I-1),"&",K.substr(J+1)].join("")
}return L.split("&")
}var E=null;
var D={};
var C={};
var F=[];
var A={0:false,10:true,13:true,34:true,39:true,60:true,62:true,92:true,8232:true,8233:true};
function B(I,J){return String.fromCharCode(J)
}function H(I){D=I["core.util"]||{}
}if(gadgets.config){gadgets.config.register("core.util",null,H)
}return{getUrlParameters:function(Q){if(E!==null&&typeof Q==="undefined"){return E
}var M={};
E={};
var J=G(Q||document.location.href);
var O=window.decodeURIComponent?decodeURIComponent:unescape;
for(var L=0,K=J.length;
L<K;
++L){var N=J[L].indexOf("=");
if(N===-1){continue
}var I=J[L].substring(0,N);
var P=J[L].substring(N+1);
P=P.replace(/\+/g," ");
M[I]=O(P)
}if(typeof Q==="undefined"){E=M
}return M
},makeClosure:function(L,N,M){var K=[];
for(var J=2,I=arguments.length;
J<I;
++J){K.push(arguments[J])
}return function(){var O=K.slice();
for(var Q=0,P=arguments.length;
Q<P;
++Q){O.push(arguments[Q])
}return N.apply(L,O)
}
},makeEnum:function(J){var L={};
for(var K=0,I;
(I=J[K]);
++K){L[I]=I
}return L
},getFeatureParameters:function(I){return typeof D[I]==="undefined"?null:D[I]
},hasFeature:function(I){return typeof D[I]!=="undefined"
},getServices:function(){return C
},registerOnLoadHandler:function(I){F.push(I)
},runOnLoadHandlers:function(){for(var J=0,I=F.length;
J<I;
++J){F[J]()
}},escape:function(I,M){if(!I){return I
}else{if(typeof I==="string"){return gadgets.util.escapeString(I)
}else{if(typeof I==="array"){for(var L=0,J=I.length;
L<J;
++L){I[L]=gadgets.util.escape(I[L])
}}else{if(typeof I==="object"&&M){var K={};
for(var N in I){if(I.hasOwnProperty(N)){K[gadgets.util.escapeString(N)]=gadgets.util.escape(I[N],true)
}}return K
}}}}return I
},escapeString:function(M){if(!M){return M
}var J=[],L,N;
for(var K=0,I=M.length;
K<I;
++K){L=M.charCodeAt(K);
N=A[L];
if(N===true){J.push("&#",L,";")
}else{if(N!==false){J.push(M.charAt(K))
}}}return J.join("")
},unescapeString:function(I){if(!I){return I
}return I.replace(/&#([0-9]+);/g,B)
}}
}();
gadgets.util.getUrlParameters();;
var tamings___=tamings___||[];
tamings___.push(function(A){caja___.whitelistFuncs([[gadgets.util,"escapeString"],[gadgets.util,"getFeatureParameters"],[gadgets.util,"getUrlParameters"],[gadgets.util,"hasFeature"],[gadgets.util,"registerOnLoadHandler"],[gadgets.util,"unescapeString"]])
});;
gadgets.rpctx=gadgets.rpctx||{};
if(!gadgets.rpctx.wpm){gadgets.rpctx.wpm=function(){var A;
return{getCode:function(){return"wpm"
},isParentVerifiable:function(){return true
},init:function(B,C){A=C;
var D=function(E){B(gadgets.json.parse(E.data))
};
if(typeof window.addEventListener!="undefined"){window.addEventListener("message",D,false)
}else{if(typeof window.attachEvent!="undefined"){window.attachEvent("onmessage",D)
}else{gadgets.warn("wpm init failure")
}}A("..",true);
return true
},setup:function(C,B){if(C===".."){gadgets.rpc.call(C,gadgets.rpc.ACK)
}return true
},call:function(C,G,F){var E=gadgets.rpc._getTargetWin(C);
var D=gadgets.rpc.getRelayUrl(C)||gadgets.util.getUrlParameters()["parent"];
var B=gadgets.rpc.getOrigin(D);
if(B){E.postMessage(gadgets.json.stringify(F),B)
}else{gadgets.error("No relay set (used as window.postMessage targetOrigin), cannot send cross-domain message")
}return true
}}
}()
};;
;
gadgets.rpctx=gadgets.rpctx||{};
if(!gadgets.rpctx.frameElement){gadgets.rpctx.frameElement=function(){var E="__g2c_rpc";
var B="__c2g_rpc";
var D;
var C;
function A(G,K,J){try{if(K!==".."){var F=window.frameElement;
if(typeof F[E]==="function"){if(typeof F[E][B]!=="function"){F[E][B]=function(L){D(gadgets.json.parse(L))
}
}F[E](gadgets.json.stringify(J));
return 
}}else{var I=document.getElementById(G);
if(typeof I[E]==="function"&&typeof I[E][B]==="function"){I[E][B](gadgets.json.stringify(J));
return 
}}}catch(H){}return true
}return{getCode:function(){return"fe"
},isParentVerifiable:function(){return false
},init:function(F,G){D=F;
C=G;
return true
},setup:function(J,F){if(J!==".."){try{var I=document.getElementById(J);
I[E]=function(K){D(gadgets.json.parse(K))
}
}catch(H){return false
}}if(J===".."){C("..",true);
var G=function(){window.setTimeout(function(){gadgets.rpc.call(J,gadgets.rpc.ACK)
},500)
};
gadgets.util.registerOnLoadHandler(G)
}return true
},call:function(F,H,G){A(F,H,G)
}}
}()
};;
;
gadgets.rpctx=gadgets.rpctx||{};
if(!gadgets.rpctx.nix){gadgets.rpctx.nix=function(){var C="GRPC____NIXVBS_wrapper";
var D="GRPC____NIXVBS_get_wrapper";
var F="GRPC____NIXVBS_handle_message";
var B="GRPC____NIXVBS_create_channel";
var A=10;
var J=500;
var I={};
var H;
var G=0;
function E(){var L=I[".."];
if(L){return 
}if(++G>A){gadgets.warn("Nix transport setup failed, falling back...");
H("..",false);
return 
}if(!L&&window.opener&&"GetAuthToken" in window.opener){L=window.opener;
if(L.GetAuthToken()==gadgets.rpc.getAuthToken("..")){var K=gadgets.rpc.getAuthToken("..");
L.CreateChannel(window[D]("..",K),K);
I[".."]=L;
window.opener=null;
H("..",true);
return 
}}window.setTimeout(function(){E()
},J)
}return{getCode:function(){return"nix"
},isParentVerifiable:function(){return false
},init:function(L,M){H=M;
if(typeof window[D]!=="unknown"){window[F]=function(O){window.setTimeout(function(){L(gadgets.json.parse(O))
},0)
};
window[B]=function(O,Q,P){if(gadgets.rpc.getAuthToken(O)===P){I[O]=Q;
H(O,true)
}};
var K="Class "+C+"\n Private m_Intended\nPrivate m_Auth\nPublic Sub SetIntendedName(name)\n If isEmpty(m_Intended) Then\nm_Intended = name\nEnd If\nEnd Sub\nPublic Sub SetAuth(auth)\n If isEmpty(m_Auth) Then\nm_Auth = auth\nEnd If\nEnd Sub\nPublic Sub SendMessage(data)\n "+F+"(data)\nEnd Sub\nPublic Function GetAuthToken()\n GetAuthToken = m_Auth\nEnd Function\nPublic Sub CreateChannel(channel, auth)\n Call "+B+"(m_Intended, channel, auth)\nEnd Sub\nEnd Class\nFunction "+D+"(name, auth)\nDim wrap\nSet wrap = New "+C+"\nwrap.SetIntendedName name\nwrap.SetAuth auth\nSet "+D+" = wrap\nEnd Function";
try{window.execScript(K,"vbscript")
}catch(N){return false
}}return true
},setup:function(O,K){if(O===".."){E();
return true
}try{var M=document.getElementById(O);
var N=window[D](O,K);
M.contentWindow.opener=N
}catch(L){return false
}return true
},call:function(K,N,M){try{if(I[K]){I[K].SendMessage(gadgets.json.stringify(M))
}}catch(L){return false
}return true
}}
}()
};;
;
gadgets.rpctx=gadgets.rpctx||{};
if(!gadgets.rpctx.rmr){gadgets.rpctx.rmr=function(){var G=500;
var E=10;
var H={};
var B;
var I;
function K(P,N,O,M){var Q=function(){document.body.appendChild(P);
P.src="about:blank";
if(M){P.onload=function(){L(M)
}
}P.src=N+"#"+O
};
if(document.body){Q()
}else{gadgets.util.registerOnLoadHandler(function(){Q()
})
}}function C(O){if(typeof H[O]==="object"){return 
}var P=document.createElement("iframe");
var M=P.style;
M.position="absolute";
M.top="0px";
M.border="0";
M.opacity="0";
M.width="10px";
M.height="1px";
P.id="rmrtransport-"+O;
P.name=P.id;
var N=gadgets.rpc.getRelayUrl(O);
if(!N){N=gadgets.rpc.getOrigin(gadgets.util.getUrlParameters()["parent"])+"/robots.txt"
}H[O]={frame:P,receiveWindow:null,relayUri:N,searchCounter:0,width:10,waiting:true,queue:[],sendId:0,recvId:0};
if(O!==".."){K(P,N,A(O))
}D(O)
}function D(O){var Q=null;
H[O].searchCounter++;
try{var N=gadgets.rpc._getTargetWin(O);
if(O===".."){Q=N.frames["rmrtransport-"+gadgets.rpc.RPC_ID]
}else{Q=N.frames["rmrtransport-.."]
}}catch(P){}var M=false;
if(Q){M=F(O,Q)
}if(!M){if(H[O].searchCounter>E){return 
}window.setTimeout(function(){D(O)
},G)
}}function J(N,P,T,S){var O=null;
if(T!==".."){O=H[".."]
}else{O=H[N]
}if(O){if(P!==gadgets.rpc.ACK){O.queue.push(S)
}if(O.waiting||(O.queue.length===0&&!(P===gadgets.rpc.ACK&&S&&S.ackAlone===true))){return true
}if(O.queue.length>0){O.waiting=true
}var M=O.relayUri+"#"+A(N);
try{O.frame.contentWindow.location=M;
var Q=O.width==10?20:10;
O.frame.style.width=Q+"px";
O.width=Q
}catch(R){return false
}}return true
}function A(N){var O=H[N];
var M={id:O.sendId};
if(O){M.d=Array.prototype.slice.call(O.queue,0);
M.d.push({s:gadgets.rpc.ACK,id:O.recvId})
}return gadgets.json.stringify(M)
}function L(X){var U=H[X];
var Q=U.receiveWindow.location.hash.substring(1);
var Y=gadgets.json.parse(decodeURIComponent(Q))||{};
var N=Y.d||[];
var O=false;
var T=false;
var V=0;
var M=(U.recvId-Y.id);
for(var P=0;
P<N.length;
++P){var S=N[P];
if(S.s===gadgets.rpc.ACK){I(X,true);
if(U.waiting){T=true
}U.waiting=false;
var R=Math.max(0,S.id-U.sendId);
U.queue.splice(0,R);
U.sendId=Math.max(U.sendId,S.id||0);
continue
}O=true;
if(++V<=M){continue
}++U.recvId;
B(S)
}if(O||(T&&U.queue.length>0)){var W=(X==="..")?gadgets.rpc.RPC_ID:"..";
J(X,gadgets.rpc.ACK,W,{ackAlone:O})
}}function F(P,S){var O=H[P];
try{var N=false;
N="document" in S;
if(!N){return false
}N=typeof S.document=="object";
if(!N){return false
}var R=S.location.href;
if(R==="about:blank"){return false
}}catch(M){return false
}O.receiveWindow=S;
function Q(){L(P)
}if(typeof S.attachEvent==="undefined"){S.onresize=Q
}else{S.attachEvent("onresize",Q)
}if(P===".."){K(O.frame,O.relayUri,A(P),P)
}else{L(P)
}return true
}return{getCode:function(){return"rmr"
},isParentVerifiable:function(){return true
},init:function(M,N){B=M;
I=N;
return true
},setup:function(O,M){try{C(O)
}catch(N){gadgets.warn("Caught exception setting up RMR: "+N);
return false
}return true
},call:function(M,O,N){return J(M,N.s,O,N)
}}
}()
};;
;
gadgets.rpctx=gadgets.rpctx||{};
if(!gadgets.rpctx.ifpc){gadgets.rpctx.ifpc=function(){var E=[];
var D=0;
var C;
function B(H){var F=[];
for(var I=0,G=H.length;
I<G;
++I){F.push(encodeURIComponent(gadgets.json.stringify(H[I])))
}return F.join("&")
}function A(I){var G;
for(var F=E.length-1;
F>=0;
--F){var J=E[F];
try{if(J&&(J.recyclable||J.readyState==="complete")){J.parentNode.removeChild(J);
if(window.ActiveXObject){E[F]=J=null;
E.splice(F,1)
}else{J.recyclable=false;
G=J;
break
}}}catch(H){}}if(!G){G=document.createElement("iframe");
G.style.border=G.style.width=G.style.height="0px";
G.style.visibility="hidden";
G.style.position="absolute";
G.onload=function(){this.recyclable=true
};
E.push(G)
}G.src=I;
window.setTimeout(function(){document.body.appendChild(G)
},0)
}return{getCode:function(){return"ifpc"
},isParentVerifiable:function(){return true
},init:function(F,G){C=G;
C("..",true);
return true
},setup:function(G,F){C(G,true);
return true
},call:function(F,K,I){var J=gadgets.rpc.getRelayUrl(F);
++D;
if(!J){gadgets.warn("No relay file assigned for IFPC");
return 
}var H=null;
if(I.l){var G=I.a;
H=[J,"#",B([K,D,1,0,B([K,I.s,"","",K].concat(G))])].join("")
}else{H=[J,"#",F,"&",K,"@",D,"&1&0&",encodeURIComponent(gadgets.json.stringify(I))].join("")
}A(H);
return true
}}
}()
};;
if(!gadgets.rpc){gadgets.rpc=function(){var T="__cb";
var S="";
var G="__ack";
var R=500;
var J=10;
var B={};
var C={};
var X={};
var K={};
var N=0;
var i={};
var W={};
var D={};
var f={};
var L={};
var V={};
var M=(window.top!==window.self);
var O=window.name;
var g=(function(){function j(k){return function(){gadgets.log("gadgets.rpc."+k+"("+gadgets.json.stringify(Array.prototype.slice.call(arguments))+"): call ignored. [caller: "+document.location+", isChild: "+M+"]")
}
}return{getCode:function(){return"noop"
},isParentVerifiable:function(){return true
},init:j("init"),setup:j("setup"),call:j("call")}
})();
if(gadgets.util){f=gadgets.util.getUrlParameters()
}var a=(f.rpc_earlyq==="1");
function A(){return typeof window.postMessage==="function"?gadgets.rpctx.wpm:typeof window.postMessage==="object"?gadgets.rpctx.wpm:window.ActiveXObject?gadgets.rpctx.nix:navigator.userAgent.indexOf("WebKit")>0?gadgets.rpctx.rmr:navigator.product==="Gecko"?gadgets.rpctx.frameElement:gadgets.rpctx.ifpc
}function b(o,m){var k=c;
if(!m){k=g
}L[o]=k;
var j=V[o]||[];
for(var l=0;
l<j.length;
++l){var n=j[l];
n.t=Y(o);
k.call(o,n.f,n)
}V[o]=[]
}function U(k){if(k&&typeof k.s==="string"&&typeof k.f==="string"&&k.a instanceof Array){if(K[k.f]){if(K[k.f]!==k.t){throw new Error("Invalid auth token. "+K[k.f]+" vs "+k.t)
}}if(k.s===G){window.setTimeout(function(){b(k.f,true)
},0);
return 
}if(k.c){k.callback=function(l){gadgets.rpc.call(k.f,T,null,k.c,l)
}
}var j=(B[k.s]||B[S]).apply(k,k.a);
if(k.c&&typeof j!=="undefined"){gadgets.rpc.call(k.f,T,null,k.c,j)
}}}function e(l){if(!l){return""
}l=l.toLowerCase();
if(l.indexOf("//")==0){l=window.location.protocol+l
}if(l.indexOf("://")==-1){l=window.location.protocol+"//"+l
}var m=l.substring(l.indexOf("://")+3);
var j=m.indexOf("/");
if(j!=-1){m=m.substring(0,j)
}var o=l.substring(0,l.indexOf("://"));
var n="";
var p=m.indexOf(":");
if(p!=-1){var k=m.substring(p+1);
m=m.substring(0,p);
if((o==="http"&&k!=="80")||(o==="https"&&k!=="443")){n=":"+k
}}return o+"://"+m+n
}function I(k){if(typeof k==="undefined"||k===".."){return window.parent
}k=String(k);
var j=window.frames[k];
if(j){return j
}j=document.getElementById(k);
if(j&&j.contentWindow){return j.contentWindow
}return null
}var c=A();
B[S]=function(){gadgets.warn("Unknown RPC service: "+this.s)
};
B[T]=function(k,j){var l=i[k];
if(l){delete i[k];
l(j)
}};
function P(l,j){if(W[l]===true){return 
}if(typeof W[l]==="undefined"){W[l]=0
}var k=document.getElementById(l);
if(l===".."||k!=null){if(c.setup(l,j)===true){W[l]=true;
return 
}}if(W[l]!==true&&W[l]++<J){window.setTimeout(function(){P(l,j)
},R)
}else{L[l]=g;
W[l]=true
}}function F(k,n){if(typeof D[k]==="undefined"){D[k]=false;
var m=gadgets.rpc.getRelayUrl(k);
if(e(m)!==e(window.location.href)){return false
}var l=I(k);
try{D[k]=l.gadgets.rpc.receiveSameDomain
}catch(j){gadgets.error("Same domain call failed: parent= incorrectly set.")
}}if(typeof D[k]==="function"){D[k](n);
return true
}return false
}function H(k,j,l){C[k]=j;
X[k]=!!l
}function Y(j){return K[j]
}function E(j,k){k=k||"";
K[j]=String(k);
P(j,k)
}function Q(j){function l(o){var q=o?o.rpc:{};
var n=q.parentRelayUrl;
if(n.substring(0,7)!=="http://"&&n.substring(0,8)!=="https://"&&n.substring(0,2)!=="//"){if(typeof f.parent==="string"&&f.parent!==""){if(n.substring(0,1)!=="/"){var m=f.parent.lastIndexOf("/");
n=f.parent.substring(0,m+1)+n
}else{n=e(f.parent)+n
}}}var p=!!q.useLegacyProtocol;
H("..",n,p);
if(p){c=gadgets.rpctx.ifpc;
c.init(U,b)
}E("..",j)
}var k={parentRelayUrl:gadgets.config.NonEmptyStringValidator};
gadgets.config.register("rpc",k,l)
}function Z(l,j){var k=j||f.parent;
if(k){H("..",k);
E("..",l)
}}function d(j,n,p){if(!gadgets.util){return 
}var m=document.getElementById(j);
if(!m){throw new Error("Cannot set up gadgets.rpc receiver with ID: "+j+", element not found.")
}var k=n||m.src;
H(j,k);
var o=gadgets.util.getUrlParameters(m.src);
var l=p||o.rpctoken;
E(j,l)
}function h(j,l,m){if(j===".."){var k=m||f.rpctoken||f.ifpctok||"";
if(window.__isgadget===true){Q(k)
}else{Z(k,l)
}}else{d(j,l,m)
}}return{register:function(k,j){if(k===T||k===G){throw new Error("Cannot overwrite callback/ack service")
}if(k===S){throw new Error("Cannot overwrite default service: use registerDefault")
}B[k]=j
},unregister:function(j){if(j===T||j===G){throw new Error("Cannot delete callback/ack service")
}if(j===S){throw new Error("Cannot delete default service: use unregisterDefault")
}delete B[j]
},registerDefault:function(j){B[S]=j
},unregisterDefault:function(){delete B[S]
},forceParentVerifiable:function(){if(!c.isParentVerifiable()){c=gadgets.rpctx.ifpc
}},call:function(j,k,p,n){j=j||"..";
var o="..";
if(j===".."){o=O
}++N;
if(p){i[N]=p
}var m={s:k,f:o,c:p?N:0,a:Array.prototype.slice.call(arguments,3),t:K[j],l:X[j]};
if(j!==".."&&!document.getElementById(j)){gadgets.log("WARNING: attempted send to nonexistent frame: "+j);
return 
}if(F(j,m)){return 
}var l=L[j]?L[j]:c;
if(!l){if(!V[j]){V[j]=[m]
}else{V[j].push(m)
}return 
}if(X[j]){l=gadgets.rpctx.ifpc
}if(l.call(j,o,m)===false){L[j]=g;
c.call(j,o,m)
}},getRelayUrl:function(k){var j=C[k];
if(j&&j.indexOf("//")==0){j=document.location.protocol+j
}return j
},setRelayUrl:H,setAuthToken:E,setupReceiver:h,getAuthToken:Y,getRelayChannel:function(){return c.getCode()
},receive:function(j){if(j.length>4){U(gadgets.json.parse(decodeURIComponent(j[j.length-1])))
}},receiveSameDomain:function(j){j.a=Array.prototype.slice.call(j.a);
window.setTimeout(function(){U(j)
},0)
},getOrigin:e,init:function(){if(c.init(U,b)===false){c=g
}if(M){h("..")
}},_getTargetWin:I,ACK:G,RPC_ID:O}
}();
gadgets.rpc.init()
};;
gadgets.config.init({"rpc":{"parentRelayUrl":"/rpc_relay.html"}});
var friendconnect_serverBase = "http://www.google.com";var friendconnect_loginUrl = "https://www.google.com/accounts";var friendconnect_gadgetPrefix = "http://www.a.friendconnect.gmodules.com/gadgets";
var friendconnect_serverVersion = "0.548.6";
var friendconnect_imageUrl = "http://www.google.com/friendconnect/scs/images";
var friendconnect_lightbox = true;
function fca(a){throw a;}var fcb=true,fcc=null,fcd=false,fce=gadgets,fcf=Error,fcg=undefined,fch=friendconnect_serverBase,fci=encodeURIComponent,fcaa=parseInt,fcj=String,fck=window,fcba=setTimeout,fcca=Object,fcl=document,fcm=Array,fcn=Math;function fcda(a,b){return a.toString=b}function fcea(a,b){return a.length=b}function fcfa(a,b){return a.className=b}function fco(a,b){return a.width=b}function fcp(a,b){return a.innerHTML=b}function fcq(a,b){return a.height=b}
var fcr="appendChild",fcs="push",fcga="toString",fct="length",fcha="propertyIsEnumerable",fcia="stringify",fc="prototype",fcja="test",fcu="width",fcv="round",fcw="slice",fcx="replace",fcy="document",fcka="data",fcz="split",fcA="getElementById",fcla="offsetWidth",fcB="charAt",fcC="location",fcD="getUrlParameters",fcE="indexOf",fcma="Dialog",fcF="style",fcna="body",fcG="left",fcH="call",fcI="match",fcJ="options",fcoa="random",fcK="createElement",fcpa="json",fcqa="addEventListener",fcra="bottom",fcL=
"setAttribute",fcsa="href",fcM="util",fcta="maxHeight",fcua="type",fcN="apply",fcva="auth",fcwa="reset",fcxa="getSecurityToken",fcO="name",fcP="parentNode",fcya="display",fcQ="height",fcza="offsetHeight",fcR="register",fcS="join",fcAa="toLowerCase",fcT="right",goog=goog||{},fcU=this,fcCa=function(a,b,c){a=a[fcz](".");c=c||fcU;!(a[0]in c)&&c.execScript&&c.execScript("var "+a[0]);for(var d;a[fct]&&(d=a.shift());)if(!a[fct]&&fcBa(b))c[d]=b;else c=c[d]?c[d]:(c[d]={})},fcDa=function(a){var b=typeof a;
if(b=="object")if(a){if(a instanceof fcm||!(a instanceof fcca)&&fcca[fc][fcga][fcH](a)=="[object Array]"||typeof a[fct]=="number"&&typeof a.splice!="undefined"&&typeof a[fcha]!="undefined"&&!a[fcha]("splice"))return"array";if(!(a instanceof fcca)&&(fcca[fc][fcga][fcH](a)=="[object Function]"||typeof a[fcH]!="undefined"&&typeof a[fcha]!="undefined"&&!a[fcha]("call")))return"function"}else return"null";else if(b=="function"&&typeof a[fcH]=="undefined")return"object";return b},fcBa=function(a){return a!==
fcg},fcEa=function(a){var b=fcDa(a);return b=="array"||b=="object"&&typeof a[fct]=="number"},fcV=function(a){return typeof a=="string"},fcFa=function(a){a=fcDa(a);return a=="object"||a=="array"||a=="function"};"closure_uid_"+fcn.floor(fcn[fcoa]()*2147483648)[fcga](36);
var fcGa=function(a){var b=fcDa(a);if(b=="object"||b=="array"){if(a.clone)return a.clone();b=b=="array"?[]:{};for(var c in a)b[c]=fcGa(a[c]);return b}return a},fcW=function(a,b){var c=b||fcU;if(arguments[fct]>2){var d=fcm[fc][fcw][fcH](arguments,2);return function(){var e=fcm[fc][fcw][fcH](arguments);fcm[fc].unshift[fcN](e,d);return a[fcN](c,e)}}else return function(){return a[fcN](c,arguments)}},fcHa=function(a){var b=fcm[fc][fcw][fcH](arguments,1);return function(){var c=fcm[fc][fcw][fcH](arguments);
c.unshift[fcN](c,b);return a[fcN](this,c)}},fcIa=function(a,b){for(var c in b)a[c]=b[c]},fcX=function(a,b,c){fcCa(a,b,c)},fcY=function(a,b){function c(){}c.prototype=b[fc];a.Kc=b[fc];a.prototype=new c;a[fc].constructor=a};SHA1=function(){this.c=fcm(5);this.ba=fcm(64);this.Bc=fcm(80);this.qa=fcm(64);this.qa[0]=128;for(var a=1;a<64;++a)this.qa[a]=0;this[fcwa]()};SHA1[fc].reset=function(){this.c[0]=1732584193;this.c[1]=4023233417;this.c[2]=2562383102;this.c[3]=271733878;this.c[4]=3285377520;this.wa=this.z=0};SHA1[fc].va=function(a,b){return(a<<b|a>>>32-b)&4294967295};
SHA1[fc].L=function(a){for(var b=this.Bc,c=0;c<64;c+=4){var d=a[c]<<24|a[c+1]<<16|a[c+2]<<8|a[c+3];b[c/4]=d}for(c=16;c<80;++c)b[c]=this.va(b[c-3]^b[c-8]^b[c-14]^b[c-16],1);a=this.c[0];d=this.c[1];var e=this.c[2],h=this.c[3],i=this.c[4],j,k;for(c=0;c<80;++c){if(c<40)if(c<20){j=h^d&(e^h);k=1518500249}else{j=d^e^h;k=1859775393}else if(c<60){j=d&e|h&(d|e);k=2400959708}else{j=d^e^h;k=3395469782}j=this.va(a,5)+j+i+k+b[c]&4294967295;i=h;h=e;e=this.va(d,30);d=a;a=j}this.c[0]=this.c[0]+a&4294967295;this.c[1]=
this.c[1]+d&4294967295;this.c[2]=this.c[2]+e&4294967295;this.c[3]=this.c[3]+h&4294967295;this.c[4]=this.c[4]+i&4294967295};SHA1[fc].update=function(a,b){if(!b)b=a[fct];var c=0;if(this.z==0)for(;c+64<b;){this.L(a[fcw](c,c+64));c+=64;this.wa+=64}for(;c<b;){this.ba[this.z++]=a[c++];++this.wa;if(this.z==64){this.z=0;for(this.L(this.ba);c+64<b;){this.L(a[fcw](c,c+64));c+=64;this.wa+=64}}}};
SHA1[fc].digest=function(){var a=fcm(20),b=this.wa*8;this.z<56?this.update(this.qa,56-this.z):this.update(this.qa,64-(this.z-56));for(var c=63;c>=56;--c){this.ba[c]=b&255;b>>>=8}this.L(this.ba);for(c=b=0;c<5;++c)for(var d=24;d>=0;d-=8)a[b++]=this.c[c]>>d&255;return a};G_HMAC=function(a,b,c){if(!a||typeof a!="object"||!a[fcwa]||!a.update||!a.digest)fca(fcf("Invalid hasher object. Hasher unspecified or does not implement expected interface."));if(b.constructor!=fcm)fca(fcf("Invalid key."));if(c&&typeof c!="number")fca(fcf("Invalid block size."));this.k=a;this.aa=c||16;this.Rb=fcm(this.aa);this.Qb=fcm(this.aa);if(b[fct]>this.aa){this.k.update(b);b=this.k.digest()}for(c=0;c<this.aa;c++){a=c<b[fct]?b[c]:0;this.Rb[c]=a^G_HMAC.OPAD;this.Qb[c]=a^G_HMAC.IPAD}};
G_HMAC.OPAD=92;G_HMAC.IPAD=54;G_HMAC[fc].reset=function(){this.k[fcwa]();this.k.update(this.Qb)};G_HMAC[fc].update=function(a){if(a.constructor!=fcm)fca(fcf("Invalid data. Data must be an array."));this.k.update(a)};G_HMAC[fc].digest=function(){var a=this.k.digest();this.k[fcwa]();this.k.update(this.Rb);this.k.update(a);return this.k.digest()};G_HMAC[fc].Fb=function(a){this[fcwa]();this.update(a);return this.digest()};var fcJa=function(a){for(var b=[],c=0,d=0;d<a[fct];d++){for(var e=a.charCodeAt(d);e>255;){b[c++]=e&255;e>>=8}b[c++]=e}return b};var fcKa=fcc,fcLa=fcc,fcMa=fcc,fcNa=fcc,fcPa=function(a,b){if(!fcEa(a))fca(fcf("encodeByteArray takes an array as a parameter"));fcOa();for(var c=b?fcMa:fcKa,d=[],e=0;e<a[fct];e+=3){var h=a[e],i=e+1<a[fct],j=i?a[e+1]:0,k=e+2<a[fct],l=k?a[e+2]:0,g=h>>2;h=(h&3)<<4|j>>4;j=(j&15)<<2|l>>6;l=l&63;if(!k){l=64;i||(j=64)}d[fcs](c[g],c[h],c[j],c[l])}return d[fcS]("")},fcQa=function(a,b){if(a[fct]%4)fca(fcf("Length of b64-encoded data must be zero mod four"));fcOa();for(var c=b?fcNa:fcLa,d=[],e=0;e<a[fct];e+=
4){var h=c[a[fcB](e)],i=c[a[fcB](e+1)],j=c[a[fcB](e+2)],k=c[a[fcB](e+3)];if(h==fcc||i==fcc||j==fcc||k==fcc)fca(fcf());h=h<<2|i>>4;d[fcs](h);if(j!=64){i=i<<4&240|j>>2;d[fcs](i);if(k!=64){j=j<<6&192|k;d[fcs](j)}}}return d},fcOa=function(){if(!fcKa){fcKa={};fcLa={};fcMa={};fcNa={};for(var a=0;a<65;a++){fcKa[a]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="[fcB](a);fcLa[fcKa[a]]=a;fcMa[a]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_."[fcB](a);fcNa[fcMa[a]]=a}}};var fcRa=function(a){for(var b=1;b<arguments[fct];b++){var c=fcj(arguments[b])[fcx](/\$/g,"$$$$");a=a[fcx](/\%s/,c)}return a},fcSa=function(a,b){var c=fcj(a)[fcAa](),d=fcj(b)[fcAa]();return c<d?-1:c==d?0:1},fcYa=function(a,b){if(b)return a[fcx](fcTa,"&amp;")[fcx](fcUa,"&lt;")[fcx](fcVa,"&gt;")[fcx](fcWa,"&quot;");else{if(!fcXa[fcja](a))return a;if(a[fcE]("&")!=-1)a=a[fcx](fcTa,"&amp;");if(a[fcE]("<")!=-1)a=a[fcx](fcUa,"&lt;");if(a[fcE](">")!=-1)a=a[fcx](fcVa,"&gt;");if(a[fcE]('"')!=-1)a=a[fcx](fcWa,
"&quot;");return a}},fcTa=/&/g,fcUa=/</g,fcVa=/>/g,fcWa=/\"/g,fcXa=/[&<>\"]/,fc_a=function(a,b){for(var c=0,d=fcj(a)[fcx](/^[\s\xa0]+|[\s\xa0]+$/g,"")[fcz]("."),e=fcj(b)[fcx](/^[\s\xa0]+|[\s\xa0]+$/g,"")[fcz]("."),h=fcn.max(d[fct],e[fct]),i=0;c==0&&i<h;i++){var j=d[i]||"",k=e[i]||"",l=RegExp("(\\d*)(\\D*)","g"),g=RegExp("(\\d*)(\\D*)","g");do{var f=l.exec(j)||["","",""],m=g.exec(k)||["","",""];if(f[0][fct]==0&&m[0][fct]==0)break;c=f[1][fct]==0?0:fcaa(f[1],10);var n=m[1][fct]==0?0:fcaa(m[1],10);c=
fcZa(c,n)||fcZa(f[2][fct]==0,m[2][fct]==0)||fcZa(f[2],m[2])}while(c==0)}return c},fcZa=function(a,b){if(a<b)return-1;else if(a>b)return 1;return 0};var fc0a,fc1a,fc2a,fc3a,fc4a,fc5a,fc6a,fc7a,fc8a,fc9a=function(){return fcU.navigator?fcU.navigator.userAgent:fcc},fc$a=function(){return fcU.navigator},fcab=function(){fc4a=fc3a=fc2a=fc1a=fc0a=fcd;var a;if(a=fc9a()){var b=fc$a();fc0a=a[fcE]("Opera")==0;fc1a=!fc0a&&a[fcE]("MSIE")!=-1;fc3a=(fc2a=!fc0a&&a[fcE]("WebKit")!=-1)&&a[fcE]("Mobile")!=-1;fc4a=!fc0a&&!fc2a&&b.product=="Gecko"}};fcab();
var fcbb=fc0a,fcZ=fc1a,fccb=fc4a,fcdb=fc2a,fceb=fc3a,fcfb=function(){var a=fc$a();return a&&a.platform||""},fcgb=fcfb(),fchb=function(){fc5a=fcgb[fcE]("Mac")!=-1;fc6a=fcgb[fcE]("Win")!=-1;fc7a=fcgb[fcE]("Linux")!=-1;fc8a=!!fc$a()&&(fc$a().appVersion||"")[fcE]("X11")!=-1};fchb();
var fcib=function(){var a="",b;if(fcbb&&fcU.opera){a=fcU.opera.version;a=typeof a=="function"?a():a}else{if(fccb)b=/rv\:([^\);]+)(\)|;)/;else if(fcZ)b=/MSIE\s+([^\);]+)(\)|;)/;else if(fcdb)b=/WebKit\/(\S+)/;if(b)a=(a=b.exec(fc9a()))?a[1]:""}return a},fcjb=fcib(),fckb={},fclb=function(a){return fckb[a]||(fckb[a]=fc_a(fcjb,a)>=0)};var fcmb=/\s*;\s*/,fcnb=function(a,b,c,d,e){if(/[;=]/[fcja](a))fca(fcf('Invalid cookie name "'+a+'"'));if(/;/[fcja](b))fca(fcf('Invalid cookie value "'+b+'"'));fcBa(c)||(c=-1);e=e?";domain="+e:"";d=d?";path="+d:"";if(c<0)c="";else if(c==0){c=new Date(1970,1,1);c=";expires="+c.toUTCString()}else{c=new Date((new Date).getTime()+c*1E3);c=";expires="+c.toUTCString()}fcl.cookie=a+"="+b+e+d+c},fcob=function(a,b){for(var c=a+"=",d=fcj(fcl.cookie)[fcz](fcmb),e=0,h;h=d[e];e++)if(h[fcE](c)==0)return h.substr(c[fct]);
return b},fcpb=function(a,b,c){var d=fcBa(fcob(a));fcnb(a,"",0,b,c);return d};var fcqb=function(a){this.stack=fcf().stack||"";if(a)this.message=fcj(a)};fcY(fcqb,fcf);fcqb[fc].name="CustomError";var fcrb=function(a,b){b.unshift(a);fcqb[fcH](this,fcRa[fcN](fcc,b));b.shift();this.messagePattern=a};fcY(fcrb,fcqb);fcrb[fc].name="AssertionError";var fcsb=function(a,b,c,d){var e="Assertion failed";if(c){e+=": "+c;var h=d}else if(a){e+=": "+a;h=b}fca(new fcrb(""+e,h||[]))},fctb=function(a,b){a||fcsb("",fcc,b,fcm[fc][fcw][fcH](arguments,2))},fcub=function(a,b){typeof a=="number"||fcsb("Expected number but got %s.",[a],b,fcm[fc][fcw][fcH](arguments,2));return a};var fc_=fcm[fc],fcvb=fc_[fcE]?function(a,b,c){fctb(a||fcV(a));fcub(a[fct]);return fc_[fcE][fcH](a,b,c)}:function(a,b,c){c=c==fcc?0:c<0?fcn.max(0,a[fct]+c):c;if(fcV(a)){if(!fcV(b)||b[fct]!=1)return-1;return a[fcE](b,c)}for(c=c;c<a[fct];c++)if(c in a&&a[c]===b)return c;return-1},fcwb=fc_.forEach?function(a,b,c){fctb(a||fcV(a));fcub(a[fct]);fc_.forEach[fcH](a,b,c)}:function(a,b,c){for(var d=a[fct],e=fcV(a)?a[fcz](""):a,h=0;h<d;h++)h in e&&b[fcH](c,e[h],h,a)},fcxb=function(a,b){return fcvb(a,b)>=0},fcyb=
function(){return fc_.concat[fcN](fc_,arguments)},fczb=function(a){if(fcDa(a)=="array")return fcyb(a);else{for(var b=[],c=0,d=a[fct];c<d;c++)b[c]=a[c];return b}},fcAb=function(a,b,c){fctb(a||fcV(a));fcub(a[fct]);return arguments[fct]<=2?fc_[fcw][fcH](a,b):fc_[fcw][fcH](a,b,c)};var fcBb=function(a,b){this.x=fcBa(a)?a:0;this.y=fcBa(b)?b:0};fcBb[fc].clone=function(){return new fcBb(this.x,this.y)};fcda(fcBb[fc],function(){return"("+this.x+", "+this.y+")"});var fc0=function(a,b){fco(this,a);fcq(this,b)};fc0[fc].clone=function(){return new fc0(this[fcu],this[fcQ])};fcda(fc0[fc],function(){return"("+this[fcu]+" x "+this[fcQ]+")"});fc0[fc].ceil=function(){fco(this,fcn.ceil(this[fcu]));fcq(this,fcn.ceil(this[fcQ]));return this};fc0[fc].floor=function(){fco(this,fcn.floor(this[fcu]));fcq(this,fcn.floor(this[fcQ]));return this};fc0[fc].round=function(){fco(this,fcn[fcv](this[fcu]));fcq(this,fcn[fcv](this[fcQ]));return this};
fc0[fc].scale=function(a){this.width*=a;this.height*=a;return this};var fcCb=function(a,b,c){for(var d in a)b[fcH](c,a[d],d,a)},fcDb=function(a){var b=[],c=0;for(var d in a)b[c++]=a[d];return b},fcEb=function(a){var b=[],c=0;for(var d in a)b[c++]=d;return b},fcFb=["constructor","hasOwnProperty","isPrototypeOf","propertyIsEnumerable","toLocaleString","toString","valueOf"],fcGb=function(a){for(var b,c,d=1;d<arguments[fct];d++){c=arguments[d];for(b in c)a[b]=c[b];for(var e=0;e<fcFb[fct];e++){b=fcFb[e];if(fcca[fc].hasOwnProperty[fcH](c,b))a[b]=c[b]}}};var fcHb=function(a){return(a=a.className)&&typeof a[fcz]=="function"?a[fcz](/\s+/):[]},fcJb=function(a){var b=fcHb(a),c=fcAb(arguments,1);c=fcIb(b,c);fcfa(a,b[fcS](" "));return c},fcIb=function(a,b){for(var c=0,d=0;d<b[fct];d++)if(!fcxb(a,b[d])){a[fcs](b[d]);c++}return c==b[fct]};var fcKb=function(a){return fcV(a)?fcl[fcA](a):a},fcLb=fcKb,fcMb=function(a,b,c,d){d=d||a;b=b&&b!="*"?b.toUpperCase():"";if(d.querySelectorAll&&(b||c)&&(!fcdb||a.compatMode=="CSS1Compat"||fclb("528"))){c=b+(c?"."+c:"");return d.querySelectorAll(c)}if(c&&d.getElementsByClassName){a=d.getElementsByClassName(c);if(b){d={};for(var e=0,h=0,i;i=a[h];h++)if(b==i.nodeName)d[e++]=i;fcea(d,e);return d}else return a}a=d.getElementsByTagName(b||"*");if(c){d={};for(h=e=0;i=a[h];h++){b=i.className;if(typeof b[fcz]==
"function"&&fcxb(b[fcz](/\s+/),c))d[e++]=i}fcea(d,e);return d}else return a},fcOb=function(a,b){fcCb(b,function(c,d){if(d=="style")a[fcF].cssText=c;else if(d=="class")fcfa(a,c);else if(d=="for")a.htmlFor=c;else if(d in fcNb)a[fcL](fcNb[d],c);else a[d]=c})},fcNb={cellpadding:"cellPadding",cellspacing:"cellSpacing",colspan:"colSpan",rowspan:"rowSpan",valign:"vAlign",height:"height",width:"width",usemap:"useMap",frameborder:"frameBorder",type:"type"},fcPb=function(a){var b=a[fcy];if(fcdb&&!fclb("500")&&
!fceb){if(typeof a.innerHeight=="undefined")a=fck;b=a.innerHeight;var c=a[fcy].documentElement.scrollHeight;if(a==a.top)if(c<b)b-=15;return new fc0(a.innerWidth,b)}a=b.compatMode=="CSS1Compat"&&(!fcbb||fcbb&&fclb("9.50"))?b.documentElement:b[fcna];return new fc0(a.clientWidth,a.clientHeight)},fc1=function(){return fcQb(fcl,arguments)},fcQb=function(a,b){var c=b[0],d=b[1];if(fcZ&&d&&(d[fcO]||d[fcua])){c=["<",c];d[fcO]&&c[fcs](' name="',fcYa(d[fcO]),'"');if(d[fcua]){c[fcs](' type="',fcYa(d[fcua]),'"');
var e={};fcGb(e,d);d=e;delete d[fcua]}c[fcs](">");c=c[fcS]("")}var h=a[fcK](c);if(d)if(fcV(d))fcfa(h,d);else fcOb(h,d);if(b[fct]>2){d=function(i){if(i)h[fcr](fcV(i)?a.createTextNode(i):i)};for(c=2;c<b[fct];c++){e=b[c];fcEa(e)&&!(fcFa(e)&&e.nodeType>0)?fcwb(fcRb(e)?fczb(e):e,d):d(e)}}return h},fcSb=function(a,b){a[fcr](b)},fcTb=function(a){return a&&a[fcP]?a[fcP].removeChild(a):fcc},fcUb=function(a,b){var c=b[fcP];c&&c.replaceChild(a,b)},fcVb=function(a,b){if(a.contains&&b.nodeType==1)return a==b||
a.contains(b);if(typeof a.compareDocumentPosition!="undefined")return a==b||Boolean(a.compareDocumentPosition(b)&16);for(;b&&a!=b;)b=b[fcP];return b==a},fcRb=function(a){if(a&&typeof a[fct]=="number")if(fcFa(a))return typeof a.item=="function"||typeof a.item=="string";else if(fcDa(a)=="function")return typeof a.item=="function";return fcd},fcWb=function(a){this.tb=a||fcU[fcy]||fcl};fcWb[fc].createElement=function(a){return this.tb[fcK](a)};fcWb[fc].createTextNode=function(a){return this.tb.createTextNode(a)};
fcWb[fc].appendChild=fcSb;fcWb[fc].removeNode=fcTb;fcWb[fc].replaceNode=fcUb;fcWb[fc].contains=fcVb;var fcXb="StopIteration"in fcU?fcU.StopIteration:fcf("StopIteration"),fcYb=function(){};fcYb[fc].next=function(){fca(fcXb)};fcYb[fc].__iterator__=function(){return this};var fc2=function(a){this.i={};this.e=[];var b=arguments[fct];if(b>1){if(b%2)fca(fcf("Uneven number of arguments"));for(var c=0;c<b;c+=2)this.set(arguments[c],arguments[c+1])}else a&&this.jb(a)};fc2[fc].q=0;fc2[fc].J=0;fc2[fc].Ka=function(){return this.q};fc2[fc].ja=function(){this.K();for(var a=[],b=0;b<this.e[fct];b++){var c=this.e[b];a[fcs](this.i[c])}return a};fc2[fc].P=function(){this.K();return this.e.concat()};fc2[fc].qb=function(a){return fcZb(this.i,a)};
fc2[fc].clear=function(){this.i={};fcea(this.e,0);this.J=this.q=0};fc2[fc].remove=function(a){if(fcZb(this.i,a)){delete this.i[a];this.q--;this.J++;this.e[fct]>2*this.q&&this.K();return fcb}return fcd};fc2[fc].K=function(){if(this.q!=this.e[fct]){for(var a=0,b=0;a<this.e[fct];){var c=this.e[a];if(fcZb(this.i,c))this.e[b++]=c;a++}fcea(this.e,b)}if(this.q!=this.e[fct]){var d={};for(b=a=0;a<this.e[fct];){c=this.e[a];if(!fcZb(d,c)){this.e[b++]=c;d[c]=1}a++}fcea(this.e,b)}};
fc2[fc].get=function(a,b){if(fcZb(this.i,a))return this.i[a];return b};fc2[fc].set=function(a,b){if(!fcZb(this.i,a)){this.q++;this.e[fcs](a);this.J++}this.i[a]=b};fc2[fc].jb=function(a){var b;if(a instanceof fc2){b=a.P();a=a.ja()}else{b=fcEb(a);a=fcDb(a)}for(var c=0;c<b[fct];c++)this.set(b[c],a[c])};fc2[fc].clone=function(){return new fc2(this)};
fc2[fc].__iterator__=function(a){this.K();var b=0,c=this.e,d=this.i,e=this.J,h=this,i=new fcYb;i.next=function(){for(;;){if(e!=h.J)fca(fcf("The map has changed since the iterator was created"));if(b>=c[fct])fca(fcXb);var j=c[b++];return a?j:d[j]}};return i};var fcZb=function(a,b){return fcca[fc].hasOwnProperty[fcH](a,b)};var fc_b=function(a,b,c,d){this.top=a;this.right=b;this.bottom=c;this.left=d};fc_b[fc].clone=function(){return new fc_b(this.top,this[fcT],this[fcra],this[fcG])};fcda(fc_b[fc],function(){return"("+this.top+"t, "+this[fcT]+"r, "+this[fcra]+"b, "+this[fcG]+"l)"});fc_b[fc].contains=function(a){return fc0b(this,a)};fc_b[fc].expand=function(a,b,c,d){if(fcFa(a)){this.top-=a.top;this.right+=a[fcT];this.bottom+=a[fcra];this.left-=a[fcG]}else{this.top-=a;this.right+=b;this.bottom+=c;this.left-=d}return this};
var fc0b=function(a,b){if(!a||!b)return fcd;if(b instanceof fc_b)return b[fcG]>=a[fcG]&&b[fcT]<=a[fcT]&&b.top>=a.top&&b[fcra]<=a[fcra];return b.x>=a[fcG]&&b.x<=a[fcT]&&b.y>=a.top&&b.y<=a[fcra]};var fc1b=function(a,b,c,d){this.left=a;this.top=b;fco(this,c);fcq(this,d)};fc1b[fc].clone=function(){return new fc1b(this[fcG],this.top,this[fcu],this[fcQ])};fcda(fc1b[fc],function(){return"("+this[fcG]+", "+this.top+" - "+this[fcu]+"w x "+this[fcQ]+"h)"});fc1b[fc].contains=function(a){return a instanceof fc1b?this[fcG]<=a[fcG]&&this[fcG]+this[fcu]>=a[fcG]+a[fcu]&&this.top<=a.top&&this.top+this[fcQ]>=a.top+a[fcQ]:a.x>=this[fcG]&&a.x<=this[fcG]+this[fcu]&&a.y>=this.top&&a.y<=this.top+this[fcQ]};var fc3b=function(a,b,c){fcV(b)?fc2b(a,c,b):fcCb(b,fcHa(fc2b,a))},fc2b=function(a,b,c){a[fcF][fc4b(c)]=b},fc5b=function(a,b){var c=a.nodeType==9?a:a.ownerDocument||a[fcy];if(c.defaultView&&c.defaultView.getComputedStyle)if(c=c.defaultView.getComputedStyle(a,""))return c[b];return fcc},fc8b=function(a,b,c){if(b instanceof fc0){c=b[fcQ];b=b[fcu]}else{if(c==fcg)fca(fcf("missing height argument"));c=c}fc6b(a,b);fc7b(a,c)},fc9b=function(a,b,c,d){if(typeof d=="number")d=(b?fcn[fcv](d):d)+"px";c[fcF][a]=
d},fc7b=fcHa(fc9b,"height",fcb),fc6b=fcHa(fc9b,"width",fcb),fc$b=function(a){var b=fcbb&&!fclb("10");if((fc5b(a,"display")||(a.currentStyle?a.currentStyle[fcya]:fcc)||a[fcF][fcya])!="none")return b?new fc0(a[fcla]||a.clientWidth,a[fcza]||a.clientHeight):new fc0(a[fcla],a[fcza]);var c=a[fcF],d=c[fcya],e=c.visibility,h=c.position;c.visibility="hidden";c.position="absolute";c.display="inline";if(b){b=a[fcla]||a.clientWidth;a=a[fcza]||a.clientHeight}else{b=a[fcla];a=a[fcza]}c.display=d;c.position=h;c.visibility=
e;return new fc0(b,a)},fcac={},fc4b=function(a){return fcac[a]||(fcac[a]=fcj(a)[fcx](/\-([a-z])/g,function(b,c){return c.toUpperCase()}))},fcbc=function(a,b){a[fcF].display=b?"":"none"};var fccc={},fcdc={};var fcec=function(a,b,c,d){b=b||"800";c=c||"550";d=d||"friendconnect";a=fck.open(a,d,"menubar=no,toolbar=no,dialog=yes,location=yes,alwaysRaised=yes,width="+b+",height="+c+",resizable=yes,scrollbars=1,status=1");fck.focus&&a&&a.focus()},fcfc=function(a,b){var c=fce[fcM][fcD]().communityId;fce.rpc[fcH](fcc,"signin",fcc,c,a,b)};fcX("goog.peoplesense.util.openPopup",fcec);fcX("goog.peoplesense.util.finishSignIn",fcfc);var fcic=function(a,b){var c=fcgc()+"/friendconnect/invite/friends",d=fci(shindig[fcva][fcxa]());fchc(c,d,a,b)},fchc=function(a,b,c,d){a+="?st="+b;if(c)a+="&customMessage="+fci(c);if(d)a+="&customInviteUrl="+fci(d);b=760;if(fcZ)b+=25;fcec(a,fcj(b),"515","friendconnect_invite")};fcX("goog.peoplesense.util.invite",fcic);fcX("goog.peoplesense.util.inviteFriends",fchc);var fcjc=function(a){this.url=a};fcjc[fc].l=function(a,b){if(this.url[fcE]("?"+a+"=")>=0||this.url[fcE]("&"+a+"=")>=0)fca(fcf("duplicate: "+a));if(b===fcc||b===fcg)return this;var c=this.url[fcE]("?")>=0?"&":"?";this.url+=c+a+"="+fci(b);return this};fcda(fcjc[fc],function(){return this.url});var fcgc=function(){return fck.friendconnect_serverBase},fckc=function(a,b,c,d,e,h,i){b=b||"800";c=c||"550";d=d||"friendconnect";h=h||fcd;fce.rpc[fcH](fcc,"openLightboxIframe",i,a,shindig[fcva][fcxa](),b,c,d,e,fcc,fcc,fcc,h)},fclc=function(a,b){var c=fce[fcM][fcD]().psinvite||"",d=new fcjc(fcgc()+"/friendconnect/signin/home");d.l("st",fck.shindig[fcva][fcxa]());d.l("psinvite",c);d.l("iframeId",a);d.l("loginProvider",b);d.l("subscribeOnSignin","1");fcec(d[fcga]());return fcd},fcmc=function(){var a=
fce[fcM][fcD]().communityId;fce.rpc[fcH](fcc,"signout",fcc,a)},fcoc=function(a,b){var c=fcgc()+"/friendconnect/settings/edit?st="+fci(shindig[fcva][fcxa]())+(a?"&iframeId="+fci(a):"");if(b)c=c+"&"+b;fcnc(c)},fcpc=function(a){a=fcgc()+"/friendconnect/settings/siteProfile?st="+fci(a);fcnc(a)},fcnc=function(a){var b=800,c=510;if(fcZ)b+=25;fcec(a,fcj(b),fcj(c))},fcqc=function(a,b,c,d){d=d||2;var e=fcc;if(b=="text"){e=fc1("div",{"class":"gfc-button-text"},fc1("div",{"class":"gfc-icon"},fc1("a",{href:"javascript:void(0);"},
c)));a[fcr](e)}else if(b=="long"||b=="standard"){e=d==1?fc1("div",{"class":"gfc-inline-block gfc-primaryactionbutton gfc-button-base"},fc1("div",{"class":"gfc-inline-block gfc-button-base-outer-box"},fc1("div",{"class":"gfc-inline-block gfc-button-base-inner-box"},fc1("div",{"class":"gfc-button-base-pos"},fc1("div",{"class":"gfc-button-base-top-shadow",innerHTML:"&nbsp;"}),fc1("div",{"class":"gfc-button-base-content"},fc1("div",{"class":"gfc-icon"},c)))))):fc1("table",{"class":"gfc-button-base-v2 gfc-button",
cellpadding:"0",cellspacing:"0"},fc1("tbody",{"class":""},fc1("tr",{"class":""},fc1("td",{"class":"gfc-button-base-v2 gfc-button-1"}),fc1("td",{"class":"gfc-button-base-v2 gfc-button-2"},c),fc1("td",{"class":"gfc-button-base-v2 gfc-button-3"}))));a[fcr](e);if(b=="standard"){b=fc1("div",{"class":"gfc-footer-msg"},"with Google Friend Connect");d==1&&a[fcr](fc1("br"));a[fcr](b)}}return e},fcrc=function(a,b){if(!a)fca("google.friendconnect.renderSignInButton: missing options");var c=a[fcF]||"standard",
d=a.text,e=a.version;if(c=="standard")d=a.text||"Sign in";else if(c=="text"||c=="long")d=a.text||"Sign in with Friend Connect";var h=a.element;if(!h){h=a.id;if(!h)fca("google.friendconnect.renderSignInButton: options[id] and options[element] == null");h=fcLb(h);if(!h)fca("google.friendconnect.renderSignInButton: element "+a.id+" not found")}fcp(h,"");c=fcqc(h,c,d,e);fck[fcqa]?c[fcqa]("click",b,fcd):c.attachEvent("onclick",b)},fcsc=function(a,b){b=b||fcW(fclc,fcc,fcc,fcc,fcc);fcrc(a,b)},fctc=function(a,
b){fce.rpc[fcH](fcc,"putReloadViewParam",fcc,a,b);var c=fce.views.getParams();c[a]=b},fcuc=function(a,b){var c=new fcjc("/friendconnect/gadgetshare/friends");c.l("customMessage",a);c.l("customInviteUrl",b);c.l("container","glb");var d=310;if(fcZ)d+=25;fckc(c[fcga](),fcj(d),"370")};fcX("goog.peoplesense.util.getBaseUrl",fcgc);fcX("goog.peoplesense.util.finishSignIn",fcfc);fcX("goog.peoplesense.util.signout",fcmc);fcX("goog.peoplesense.util.signin",fclc);fcX("goog.peoplesense.util.editSettings",fcoc);
fcX("goog.peoplesense.util.editSSProfile",fcpc);fcX("goog.peoplesense.util.setStickyViewParamToken",fctc);fcX("google.friendconnect.renderSignInButton",fcsc);fcX("goog.peoplesense.util.share",fcuc);fcX("goog.peoplesense.util.userAgent.IE",fcZ);var fcvc={},fcwc={},fc3=function(a){this.h=new fc2;this.snippetId=a.id;this.site=a.site;a=a["view-params"];var b=a.skin;this.bc=(b?b.POSITION:"top")||"top";this.Cc={allowAnonymousPost:a.allowAnonymousPost||fcd,scope:a.scope||"SITE",docId:a.docId||"",features:a.features||"video,comment",startMaximized:"true",disableMinMax:"true",skin:b};this.absoluteBottom=fcZ&&!fclb("7");this.fixedIeSizes=fcZ;fck[fcqa]?fck[fcqa]("resize",fcW(this.$a,this),fcd):fck.attachEvent("onresize",fcW(this.$a,this));this.ob()};
fc3[fc].ob=function(){if(!this.site)fca(fcf("Must supply site ID."));if(!this.snippetId)fca(fcf("Must supply a snippet ID."))};fc3[fc].b=10;fc3[fc].za=1;fc3[fc].p="fc-friendbar-";fc3[fc].t=fc3[fc].p+"outer";fc3[fc].cb=fc3[fc].t+"-shadow";fc3[fc].render=function(){fcl.write(this.xb());var a=fcKb(this.snippetId);fcp(a,this.N())};fc3[fc].yb=function(){var a=fcKb(this.t);return a=fc$b(a)[fcu]};fc3[fc].$a=function(){for(var a=this.h.P(),b=0;b<a[fct];b++)this.nc(a[b]);goog&&fccc&&fcdc&&fcxc&&fcyc("resize")};
fc3[fc].n=function(){return this.bc};fc3[fc].d=function(a){return this.p+"shadow-"+a};fc3[fc].ha=function(a){return this.p+"menus-"+a};fc3[fc].Q=function(a){return this.p+a+"Target"};fc3[fc].fa=function(a){return this.p+a+"Drawer"};fc3[fc].Pa=function(){return this.Q("")};fc3[fc].Qa=function(){return this.p+"wallpaper"};fc3[fc].La=function(){return this.fa("")};
fc3[fc].xb=function(){var a=fck.friendconnect_imageUrl+"/",b=a+"shadow_tc.png",c=a+"shadow_bc.png",d=a+"shadow_bl.png",e=a+"shadow_tl.png",h=a+"shadow_tr.png",i=a+"shadow_br.png";a=a+"shadow_cr.png";var j=function(m,n){return fcZ?'filter: progid:DXImageTransform.Microsoft.AlphaImageLoader(src="'+m+'", sizingMethod="scale");':"background-image: url("+m+");background-repeat: "+n+"; "},k="position:absolute; top:";if(this.n()!="top"){k="position:fixed; bottom:";if(this.absoluteBottom)k="position:absolute; bottom:"}var l=
c;if(this.n()!="top")l=b;var g=0,f=[];f[g++]='<style type="text/css">';if(this.n()!="top"&&this.absoluteBottom)f[g++]="html, body {height: 100%; overflow: auto; };";f[g++]="#"+this.t+" {";f[g++]="background:#E0ECFF;";f[g++]="left:0;";f[g++]="height: "+(fcZ?"35px;":"36px;");if(this.n()!="top"&&this.absoluteBottom)f[g++]="margin-right: 20px;";f[g++]="padding:0;";f[g++]=k+" 0;";f[g++]="width:100%;";f[g++]="z-index:5000;";f[g++]="}";f[g++]="#"+this.cb+" {";f[g++]=j(l,"repeat-x");f[g++]="left:0;";f[g++]=
"height:"+this.b+"px;";if(this.n()!="top"&&this.absoluteBottom)f[g++]="margin-right: 20px;";f[g++]="padding:0;";f[g++]=k+(fcZ?"35px;":"36px;");f[g++]="width:100%;";f[g++]="z-index:4998;";f[g++]="}";f[g++]="."+this.La()+" {";f[g++]="display: block;";f[g++]="padding:0;";f[g++]=k+(fcZ?"34px;":"35px;");f[g++]="z-index:4999;";f[g++]="}";f[g++]="."+this.Qa()+" {";f[g++]="background: white;";f[g++]="height: 100%;";f[g++]="margin-right: "+this.b+"px;";f[g++]="}";f[g++]="."+this.Pa()+" {";f[g++]="border: "+
this.za+"px solid #ccc;";f[g++]="height: 100%;";f[g++]="left: 0;";f[g++]="background-image: url("+fck.friendconnect_imageUrl+"/loading.gif);";f[g++]="background-position: center;";f[g++]="background-repeat: no-repeat;";f[g++]="}";f[g++]="."+this.d("cr")+" {";f[g++]=j(a,"repeat-y");f[g++]="height: 100%;";f[g++]="position:absolute;";f[g++]="right: 0;";f[g++]="top: 0;";f[g++]="width:"+this.b+"px;";f[g++]="}";f[g++]="."+this.d("bl")+" {";f[g++]=j(d,"no-repeat");f[g++]="height: "+this.b+"px;";f[g++]="position:absolute;";
f[g++]="width:"+this.b+"px;";f[g++]="}";f[g++]="."+this.d("tl")+" {";f[g++]=j(e,"no-repeat");f[g++]="height: "+this.b+"px;";f[g++]="position:absolute;";f[g++]="left:0px;";f[g++]="width:"+this.b+"px;";f[g++]="}";f[g++]="."+this.d("bc")+" {";f[g++]=j(c,"repeat-x");f[g++]="height: "+this.b+"px;";f[g++]="left: "+this.b+"px;";f[g++]="position:absolute;";f[g++]="right: "+this.b+"px;";f[g++]="}";f[g++]="."+this.d("tc")+" {";f[g++]=j(b,"repeat-x");f[g++]="height: "+this.b+"px;";f[g++]="left: "+this.b+"px;";
f[g++]="margin-left: "+this.b+"px;";f[g++]="margin-right: "+this.b+"px;";f[g++]="right: "+this.b+"px;";f[g++]="}";f[g++]="."+this.d("br")+" {";f[g++]=j(i,"no-repeat");f[g++]="height: "+this.b+"px;";f[g++]="position:absolute;";f[g++]="right: 0;";f[g++]="width: "+this.b+"px;";f[g++]="}";f[g++]="."+this.d("tr")+" {";f[g++]=j(h,"no-repeat");f[g++]="height: "+this.b+"px;";f[g++]="position:absolute;";f[g++]="right: 0;";f[g++]="top: 0;";f[g++]="width: "+this.b+"px;";f[g++]="}";f[g++]="</style>";return f[fcS]("")};
fc3[fc].N=function(){var a=['<div id="'+this.t+'"></div>','<div id="'+this.cb+'"></div>','<div id="'+this.ha(this.h.Ka())+'"></div>'];return a[fcS]("")};fc3[fc].rb=function(a,b,c,d){if(!this.h.qb(a)){b=new fc4(this,a,b,c,d);c=this.h.Ka();d=fcKb(this.ha(c));fcp(d,b.N()+'<div id="'+this.ha(c+1)+'"></div>');this.h.set(a,b)}};fc3[fc].la=function(a){(a=this.h.get(a))&&a.drawer&&fcbc(a.drawer,fcd)};fc3[fc].dc=function(a){if(a=this.h.get(a))a.rendered=fcd};
fc3[fc].refresh=function(){for(var a=this.h.P(),b=0;b<a[fct];b++){var c=a[b];this.la(c);this.dc(c)}};fc3[fc].Yb=function(a){for(var b=this.h.ja(),c=0;c<b[fct];c++){var d=b[c];if(d.id==a){d.zc();break}}};fc3[fc].Xb=function(a){for(var b=this.h.ja(),c=0;c<b[fct];c++){var d=b[c];if(d.id==a){d.Ub();break}}};fc3[fc].nc=function(a){if((a=this.h.get(a))&&a.drawer&&a.na()){a.da();a.Ha();a.ya()}};
fc3[fc].yc=function(a,b){var c=this.h.get(a);if(c){if(!c.drawer){c.drawer=fcKb(this.fa(c[fcO]));c.target=fcKb(this.Q(c[fcO]));c.sha_bc=fcMb(fcl,"div",this.n()=="top"?this.d("bc"):this.d("tc"),c.drawer)[0];c.sha_cr=fcMb(fcl,"div",this.d("cr"),c.drawer)[0]}for(var d=this.h.P(),e=0;e<d[fct];e++){var h=d[e];a!==h&&this.la(h)}c.da(b);fcbc(c.drawer,fcb);fck.setTimeout(function(){c.ya();c.Ha();c.render()},0)}};
var fc4=function(a,b,c,d,e){this.id=-1;this.bar=a;this.name=b;this.constraints=d;this.skin=e||{};fcq(this,this.skin.HEIGHT||"0");this.url=fck.friendconnect_serverBase+c;this.sha_bc=this.target=this.drawer=fcc;this.loaded=this.rendered=fcd;this.da()};
fc4[fc].da=function(a){fcGb(this.constraints,a||{});fcGb(this.skin,this.constraints);if(this.bar.fixedIeSizes&&this.constraints[fcG]&&this.constraints[fcT]){a=this.bar.yb();var b=this.constraints[fcG],c=this.constraints[fcT];a=a-(b+c);if(a%2){a-=1;this.skin.right+=1}fco(this.skin,a);delete this.skin[fcG]}};
fc4[fc].ya=function(){if(this.drawer){if(this.skin[fcu]){var a=this.bar.za,b=this.bar.b,c=fcZ?2:0;fc8b(this.target,this.skin[fcu],"");fc8b(this.sha_bc,this.skin[fcu]-b+2*a-c,"");this.skin.rightShadow?fc8b(this.drawer,this.skin[fcu]+b+2*a-c,""):fc8b(this.drawer,this.skin[fcu]+2*a-c,"")}if(this.skin[fcT])this.drawer[fcF].right=this.skin[fcT]+0+"px"}};
fc4[fc].Ha=function(){if(fcZ&&this.drawer){var a=fc$b(this.target),b=a[fcu]-this.bar.b;a=a[fcQ];if(b<0)b=0;this.sha_bc&&this.sha_bc[fcF]&&fc8b(this.sha_bc,b,"");this.sha_cr&&this.sha_cr[fcF]&&fc8b(this.sha_cr,"",a)}};
fc4[fc].N=function(){var a="display:none;",b="position: relative; ",c="",d="",e="",h="",i=!!this.skin.rightShadow;if(!i){c+="display: none; ";e+="display: none; ";d+="right: 0px; ";h+="margin-right: 0px; "}for(var j in this.skin){var k=Number(this.skin[j]);if(i&&fcSa(j,"width")==0)k+=this.bar.b;if(fcSa(j,"height")==0)b+=j+": "+k+"px; ";if(j!="rightShadow"){if(fcSa(j,"height")==0)k+=this.bar.b;if(fcSa(j,"width")==0)k+=2;a+=j+": "+k+"px; "}if(fcZ&&fcSa(j,"width")==0){k-=i?2*this.bar.b:this.bar.b;d+=
j+": "+k+"px; "}}if(fcZ&&(this[fcQ]|0)>0){i=(this[fcQ]|0)+2;c+="height: "+i+"px; "}i=0;j=[];j[i++]='<div id="'+this.bar.fa(this[fcO])+'"class="'+this.bar.La()+'"style="'+a+'"> ';if(this.bar.n()=="bottom")j[i++]='<div class="'+this.bar.d("tl")+'"></div> <div class="'+this.bar.d("tc")+'"style="'+d+'"></div> <div class="'+this.bar.d("tr")+'"style="'+e+'"></div> ';j[i++]='<div style="'+b+'"> <div class="'+this.bar.Qa()+'"style="'+h+'"><div id="'+this.bar.Q(this[fcO])+'"class="'+this.bar.Pa()+'"></div> <div class="'+
this.bar.d("cr")+'"style="'+c+'"></div> </div> </div> ';if(this.bar.n()=="top")j[i++]='<div class="'+this.bar.d("bl")+'"></div> <div class="'+this.bar.d("bc")+'"style="'+d+'"></div> <div class="'+this.bar.d("br")+'"style="'+e+'"></div> ';j[i++]="</div> ";return j[fcS]("")};fc4[fc].zc=function(){this.rendered=this.na()};fc4[fc].Ub=function(){this.loaded=this.na()};fc4[fc].na=function(){return!!this.drawer&&this.drawer[fcF][fcya]!="none"};
fc4[fc].render=function(){if(this.rendered==fcd){var a={};a.url=this.url;a.id=this.bar.Q(this[fcO]);a.site=this.bar.site;a["view-params"]=fcGa(this.bar.Cc);if(this[fcO]=="profile")a["view-params"].profileId="VIEWER";this.skin&&fcGb(a["view-params"].skin,this.skin);a["view-params"].menuName=this[fcO];a["view-params"].opaque="true";a["view-params"].menuPosition=this.bar.bc;fcq(a,"1px");if(fcvc&&fcwc&&fc5)this.id=fc5.render(a)}};fcX("google.friendconnect.FriendBar",fc3);var fczc="0123456789abcdefghijklmnopqrstuv",fcBc=function(a){a=new fcAc(a);if(a.pa()%5)fca(fcf());for(var b=[],c=0;a.pa()>0;c++)b[c]=fczc[fcB](a.$b(5));return b[fcS]("")},fcAc=function(a){this.D=this.r=0;this.ca=a};fcAc[fc].pa=function(){return 8*(this.ca[fct]-this.D)-this.r};
fcAc[fc].$b=function(a){var b=0;if(a>this.pa())fca(fcf());if(this.r>0){b=255>>this.r&this.ca[this.D];var c=8-this.r,d=fcn.min(a%8,c);c=c-d;b=b>>c;a-=d;this.r+=d;if(this.r==8){this.r=0;this.D++}}for(;a>=8;){b<<=8;b|=this.ca[this.D];this.D++;a-=8}if(a>0){b<<=a;b|=this.ca[this.D]>>8-a;this.r=a}return b};var fcCc=function(){};fcCc[fc].F=function(){};fcCc[fc].I=function(){};var fcDc=(new Date).getTime(),fc6=function(){},fcEc=function(){},fcFc=function(){},fcGc=function(){};fcY(fcGc,fcFc);var fcHc=function(a){if(a)for(var b in a)if(a.hasOwnProperty(b))this[b]=a[b];if(this.viewParams)for(var c in this.viewParams)if(/^FC_RELOAD_.*$/[fcja](c))this.viewParams[c]=fcc};fcHc[fc].render=function(a){var b=this;if(a){b.Ac();this.Ab(function(c){fc3b(a,"visibility","hidden");fcp(a,c);b.refresh(a,c);c=function(d){fc3b(d,"visibility","visible")};c=fcHa(c,a);fcba(c,500);b.chrome=a})}};
fcHc[fc].Ab=function(a){return this.Gb(a)};var fc7=function(a){fcHc[fcH](this,a);this.U="../../";this.rpcToken=fcj(fcn[fcv](2147483647*fcn[fcoa]()))};fcY(fc7,fcHc);fc7[fc].hb="gfc_iframe_";fc7[fc].ib="friendconnect";fc7[fc].Ia="";fc7[fc].oc="rpc_relay.html";fc7[fc].X=function(a){this.U=a};fc7[fc].Ac=function(){return this.Ia=fcj(fcn[fcv](2147483647*fcn[fcoa]()))};fc7[fc].ga=function(){return this.hb+this.Ia+"_"+this.id};
fc7[fc].refresh=function(a,b){var c=fc5.Fc,d,e={},h=fc5.Ja(this.communityId),i=h[fcz]("~"),j=fc5.sb;if(j&&i[fct]>1){d=i[2];i=i[1];var k=[this.specUrl,this.communityId,i,j][fcS](":");e.sig=fc5.hash(d,k);e.userId=i;e.dateStamp=j}e.container=this.ib;e.mid=this.id;e.nocache=fc5.ac;e.view=this.Z;e.parent=fc5.S;if(this.debug)e.debug="1";if(this.specUrl)e.url=this.specUrl;if(this.communityId){j=fce[fcM][fcD]().profileId;e.communityId=this.communityId;if(d=fce[fcM][fcD]().psinvite)e.psinvite=d;if(j)e.profileId=
j}e.caller=fcIc();e.rpctoken=this.rpcToken;j=fcd;d="";i=/Version\/3\..*Safari/;if((i=fcdb&&fc9a()[fcI](i))||!fc5.R[this.specUrl]&&this.viewParams){e["view-params"]=fce[fcpa][fcia](this.viewParams);d="?viewParams="+fci(e["view-params"]);j=fcb}if(this.prefs)e.prefs=fce[fcpa][fcia](this.prefs);if(this.viewParams&&this.sendViewParamsToServer)e["view-params"]=fce[fcpa][fcia](this.viewParams);if(this.locale)e.locale=this.locale;if(this.secureToken)e.st=this.secureToken;i=fc5.Oa(this.specUrl);d=i+"ifr"+
d+(this.hashData?"&"+this.hashData:"");if(fc5.Ec!=1||j||h||this.secureToken){if(h&&!e.sig)e.fcauth=h}else e.sig||(c="get");h=this.ga();fcJc(h,d,c,e,a,b,this.rpcToken)};var fc8=function(){this.j={};this.S="http://"+fcl[fcC].host;this.Z="default";this.ac=1;this.Jc=0;this.Gc="US";this.Hc="en";this.Ic=2147483647};fcY(fc8,fcEc);fc8[fc].v=fcHc;fc8[fc].A=new fcGc;fc8[fc].bb=function(a){this.ac=a};fc8[fc].Ga=function(a){this.Ec=a};fc8[fc].Na=function(a){return"gadget_"+a};fc8[fc].w=function(a){return this.j[this.Na(a)]};
fc8[fc].M=function(a){return new this.v(a)};fc8[fc].kb=function(a){a.id=this.Hb();this.j[this.Na(a.id)]=a};fc8[fc].Zb=0;fc8[fc].Hb=function(){return this.Zb++};var fcLc=function(){fc8[fcH](this);this.A=new fcKc};fcY(fcLc,fc8);fcLc[fc].v=fc7;fcLc[fc].W=function(a){a[fcI](/^http[s]?:\/\//)||(a=fcl[fcC][fcsa][fcI](/^[^?#]+\//)[0]+a);this.S=a};fcLc[fc].H=function(a){var b=this.A.Ma(a);a.render(b)};var fcKc=function(){this.wb={}};fcY(fcKc,fcFc);
fcKc[fc].lb=function(a,b){this.wb[a]=b;var c=fcl[fcA](b).className;if(!c&&c[fct]==0)fcfa(fcl[fcA](b),"gadgets-gadget-container")};fcKc[fc].Ma=function(a){return(a=this.wb[a.id])?fcl[fcA](a):fcc};var fc9=function(a){fc7[fcH](this,a);a=a||{};this.Z=a.view||"profile"};fcY(fc9,fc7);fc9[fc].nb="canvas.html";fc9[fc].ub="/friendconnect/embed/";
var fcIc=function(){var a=fce[fcM][fcD]().canvas=="1"||fce[fcM][fcD]().embed=="1",b=fcc;if(a)b=fce[fcM][fcD]().caller;if(!b){a=fcl[fcC];b=a.search[fcx](/([&?]?)psinvite=[^&]*(&?)/,function(c,d,e){return e?d:""});b=a.protocol+"//"+a.hostname+(a.port?":"+a.port:"")+a.pathname+b}return b};fc9[fc].wc=function(a){this.Z=a};fc9[fc].ka=function(){return this.Z};fc9[fc].getBodyId=function(){return this.ga()+"_body"};
fc9[fc].Gb=function(a){var b=this.specUrl;if(b===fcg)b="";b=(fc5.Oa(b)||this.U)+this.oc;var c=this.ga();fce.rpc.setRelayUrl(c,b);b='<div id="'+this.getBodyId()+'"><iframe id="'+c+'" name="'+c;b+=this[fcQ]==0?'" style="width:1px; height:1px;':'" style="width:100%;';if(this.viewParams.opaque)b+="background-color:white;";b+='"';b+=' frameborder="0" scrolling="no"';this.viewParams.opaque||(b+=' allowtransparency="true"');b+=this[fcQ]?' height="'+this[fcQ]+'"':"";b+=this[fcu]?' width="'+this[fcu]+'"':
"";b+="></iframe>";if(this.showEmbedThis)b+='<a href="javascript:void(0);" onclick="google.friendconnect.container.showEmbedDialog(\''+this.divId+"'); return false;\">Embed this</a>";b+="</div>";a(b)};
fc9[fc].zb=function(){var a=fcIc();a="canvas=1&caller="+fci(a);var b=fce[fcM][fcD]().psinvite;if(b)a+="&psinvite="+fci(b);a+="&site="+fci(this.communityId);b=fcGa(this.viewParams);if(b.skin!=fcc)for(var c=["BG_IMAGE","BG_COLOR","FONT_COLOR","BG_POSITION","BG_REPEAT","ANCHOR_COLOR","FONT_FACE","BORDER_COLOR","CONTENT_BG_COLOR","CONTENT_HEADLINE_COLOR","CONTENT_LINK_COLOR","CONTENT_SECONDARY_TEXT_COLOR","CONTENT_SECONDARY_LINK_COLOR","CONTENT_TEXT_COLOR","ENDCAP_BG_COLOR","ENDCAP_LINK_COLOR","ENDCAP_TEXT_COLOR",
"CONTENT_VISITED_LINK_COLOR","ALTERNATE_BG_COLOR"],d=0;d<c[fct];d++)delete b.skin[c[d]];b=fci(fce[fcpa][fcia](b));b=b[fcx]("\\","%5C");return fc5.S+this.nb+"?url="+fci(this.specUrl)+(a?"&"+a:"")+"&view-params="+b};fc9[fc].C=function(a){a=a||fch+this.ub+this.communityId;return this.Bb(a,"embed=1")};fc9[fc].B=function(a){return'<iframe src="'+this.C(a)+'" style="height:500px" scrolling="no" allowtransparency="true" border="0" frameborder="0" ></iframe>'};
fc9[fc].Bb=function(a,b){var c=fci(fce[fcpa][fcia](this.viewParams));c=c[fcx]("\\","%5C");return a+"?url="+fci(this.specUrl)+(b?"&"+b:"")+"&view-params="+c};fc9[fc].Kb=function(){var a=fce[fcM][fcD]().canvas=="1"||fce[fcM][fcD]().embed=="1",b=fcc;if(a)(b=fce[fcM][fcD]().caller)||(b="javascript:history.go(-1)");return b};fc9[fc].Lb=function(a){var b=fcc;if(a=="canvas")b=this.zb();else if(a=="profile")b=this.Kb();return b};
var fc$=function(){fcLc[fcH](this);fce.rpc[fcR]("signin",fc6[fc].signin);fce.rpc[fcR]("signout",fc6[fc].signout);fce.rpc[fcR]("resize_iframe",fc6[fc].ab);fce.rpc[fcR]("set_title",fc6[fc].setTitle);fce.rpc[fcR]("requestNavigateTo",fc6[fc].Za);fce.rpc[fcR]("api_loaded",fc6[fc].xa);fce.rpc[fcR]("createFriendBarMenu",fc6[fc].Ca);fce.rpc[fcR]("showFriendBarMenu",fc6[fc].db);fce.rpc[fcR]("hideFriendBarMenu",fc6[fc].Ra);fce.rpc[fcR]("putReloadViewParam",fc6[fc].Va);fce.rpc[fcR]("getViewParams",fc6[fc].Fa);
fce.rpc[fcR]("getContainerBaseTime",fc6[fc].Ea);fce.rpc[fcR]("openLightboxIframe",fc6[fc].Ua);fce.rpc[fcR]("showMemberProfile",fc6[fc].fb);fce.rpc[fcR]("closeLightboxIframe",fcW(this.u,this));fce.rpc[fcR]("setLightboxIframeTitle",fcW(this.sc,this));fce.rpc[fcR]("refreshAndCloseIframeLightbox",fcW(this.cc,this));var a=fcMc;a[fcR]();a.gb(this,"load",this.Nb);a.gb(this,"start",this.Ob);this.U="../../";this.W("");this.bb(0);this.Ga(1);this.oa=fcc;this.apiVersion="0.8";this.openSocialSecurityToken=fcc;
this.V="";this.Da={};this.Tb=fcc;this.Sb=fcd;this.sb=this.Wb=this.lastIframeLightboxOpenArguments=this.lastLightboxCallback=this.lastLightboxDialog=fcc;this.Fc="post"};fcY(fc$,fcLc);fc$[fc].qc=function(a){this.sb=a};fc$[fc].v=fc9;fc$[fc].R={};fc$[fc].uc=function(a){this.oa=a};fc$[fc].Oa=function(a){var b=fc$[fc].R[a];if(!b)if(this.oa[fcE]("http://")!==0){a=this.pb(a);b=["http://",a,this.oa][fcS]("")}else b=this.oa;return b};
fc$[fc].pb=function(a){var b=new SHA1;a=fcJa(a);b.update(a);b=b.digest();return b=fcBc(b)};
var fcNc=function(a,b){var c=b?b:fck.top,d=c.frames;try{if(c.frameElement.id==a)return c}catch(e){}for(c=0;c<d[fct];++c){var h=fcNc(a,d[c]);if(h)return h}return fcc},fcJc=function(a,b,c,d,e,h,i){var j="gfc_load_"+a;b='<html><head><style type="text/css">body {background:transparent;}</style>'+(fcZ?'<script type="text/javascript">window.goback=function(){history.go(-1);};setTimeout("goback();", 0);<\/script>':"")+"</head><body><form onsubmit='window.goback=function(){};return false;' style='margin:0;padding:0;' id='"+
j+"' method='"+c+"' ' action='"+fce[fcM].escapeString(b)+"'>";for(var k in d)b+="<input type='hidden' name='"+k+"' value='' >";b+="</form></body></html>";c=fcNc(a);var l;try{l=c[fcy]||c.contentWindow[fcy]}catch(g){if(e&&h){fcp(e,"");fcp(e,h);c=fcNc(a);l=c[fcy]||c.contentWindow[fcy]}}i&&fce.rpc.setAuthToken(a,i);l.open();l.write(b);l.close();a=l[fcA](j);for(k in d)a[k].value=d[k];fcZ&&a.onsubmit();a.submit()};
fc$[fc].vb=function(){var a=fce[fcM][fcD]().fcsite,b=fce[fcM][fcD]().fcprofile;a&&b&&fc5.I(b,a)};fc$[fc].rc=function(a,b){this.R[a]=b};fc$[fc].T=function(){var a=/Version\/3\..*Safari/;if(a=fcdb&&fc9a()[fcI](a))fcl[fcC].reload();else{fc5.g!=fcc&&fc5.g.refresh();for(var b in fc5.j){a=fc5.j[b];this.H(a)}if(this.lastIframeLightboxOpenArguments!=fcc){b=this.lastIframeLightboxOpenArguments;this.u();this.F[fcN](this,b)}}};
fc$[fc].W=function(a){a[fcI](/^http[s]?:\/\//)||(a=a&&a[fct]>0&&a.substring(0,1)=="/"?fcl[fcC][fcsa][fcI](/^http[s]?:\/\/[^\/]+\//)[0]+a.substring(1):fcl[fcC][fcsa][fcI](/^[^?#]+\//)[0]+a);this.S=a};fc$[fc].ea=function(a){return"fcauth"+a};fc$[fc].ia=function(a){return"fcauth"+a+"-s"};fc$[fc].hash=function(a,b){var c=new SHA1,d=fcQa(a,fcb);c=new G_HMAC(c,d,64);d=fcJa(b);c=c.Fb(d);(new Date).getTime();return fcPa(c,fcb)};
fc$[fc].Ja=function(a){return a=fcob(this.ea(a))||fcob(this.ia(a))||this.Da[a]||""};fc$[fc].X=function(a){this.U=a};fc$[fc].vc=function(a){this.V=a};fc$[fc].M=function(a){a=new this.v(a);a.X(this.U);return a};fc$[fc].ka=function(){return this.Z};fc$[fc].tc=function(a){this.Wb=a};var fcOc=function(a){return(a=a[fcI](/_([0-9]+)$/))?fcaa(a[1],10):fcc};
fc$[fc].Y=function(a,b,c,d,e,h){if(!this.Dc){this.$(fck.friendconnect_serverBase+"/friendconnect/styles/container.css?d="+this.V);this.Dc=fcb}var i=fcPc(d);if(this.Tb!=(i?"rtl":"ltr")){this.$(fck.friendconnect_serverBase+"/friendconnect/styles/lightbox"+(i?"-rtl":"")+".css?d="+this.V);this.Tb=i?"rtl":"ltr"}if(!this.Sb){this.mb(fck.friendconnect_serverBase+"/friendconnect/script/lightbox.js?d="+this.V);this.Sb=fcb}b=b||0;if(goog.ui&&goog.ui[fcma]){this.u();b=new goog.ui[fcma]("lightbox-dialog",fcb);
var j=this;goog.events.listen(b,goog.ui[fcma].EventType.AFTER_HIDE,function(){j.lastLightboxCallback&&j.lastLightboxCallback();j.Ba()});b.setDraggable(fcb);b.setDisposeOnHide(fcb);b.setBackgroundElementOpacity(0.5);b.setButtonSet(new goog.ui[fcma].ButtonSet);this.lastLightboxDialog=b;this.lastLightboxCallback=c||fcc;c=b.getDialogElement();e=e||702;fc3b(c,"width",fcj(e)+"px");h&&fc3b(c,"height",fcj(h)+"px");a(b);b.getDialogElement()[fcF].direction=i?"rtl":"ltr"}else if(b<5){b++;a=fcW(this.Y,this,a,
b,c,d,e,h);fcba(a,1E3)}else{this.Ba();fca(fcf("lightbox.js failed to load"))}};fc$[fc].u=function(a){var b=this.lastLightboxDialog,c=this.lastLightboxCallback;this.lastLightboxCallback=fcc;if(b!=fcc){this.lastLightboxDialog.dispatchEvent(goog.ui[fcma].EventType.AFTER_HIDE);b.dispose();c!=fcc&&c(a)}};fc$[fc].Ba=function(){this.lastIframeLightboxOpenArguments=this.lastLightboxCallback=this.lastLightboxDialog=fcc};fc$[fc].sc=function(a){this.lastLightboxDialog&&this.lastLightboxDialog.setTitle(a)};
fc$[fc].cc=function(){this.u();this.T()};fc6[fc].Za=function(a,b){var c=fcOc(this.f);c=fc5.w(c);var d=fcGa(c.originalParams);if(b){d["view-params"]=d["view-params"]||{};d["view-params"]=b}d.locale=c.locale;if(c.useLightBoxForCanvas){d.presentation=a;fc5.lastLightboxDialog!=fcc?fc5.u():fc5.eb(d)}else if((c=c.Lb(a))&&fcl[fcC][fcsa]!=c)if(fce[fcM][fcD]().embed=="1")try{fck.parent.location=c}catch(e){fck.top.location=c}else fcl[fcC].href=c};
fc$[fc].eb=function(a,b){a=a||{};var c=a.locale,d=fcPc(c),e=this;this.u();this.Y(function(h){var i=fc1("div",{},fc1("div",{id:"gadget-signin",style:"background-color:#ffffff;height:32px;"}),fc1("div",{id:"gadget-lb-canvas",style:"background-color:#ffffff;"}));h.getTitleTextElement()[fcr](fc1("div",{id:"gfc-canvas-title",style:"color:#000000;"}));h.getContentElement()[fcr](i);h.setVisible(fcb);i=fcGa(a);var j=fcPb(fck),k=fcn[fcv](j[fcQ]*0.7);j={};j.BORDER_COLOR="#cccccc";j.ENDCAP_BG_COLOR="#e0ecff";
j.ENDCAP_TEXT_COLOR="#333333";j.ENDCAP_LINK_COLOR="#0000cc";j.ALTERNATE_BG_COLOR="#ffffff";j.CONTENT_BG_COLOR="#ffffff";j.CONTENT_LINK_COLOR="#0000cc";j.CONTENT_TEXT_COLOR="#333333";j.CONTENT_SECONDARY_LINK_COLOR="#7777cc";j.CONTENT_SECONDARY_TEXT_COLOR="#666666";j.CONTENT_HEADLINE_COLOR="#333333";i.id="gadget-lb-canvas";fcq(i,fcn.min(498,k)+"px");i.maxHeight=k;if(i.keepMax){fcq(i,k);fc3b(h.getContentElement(),"height",k+35+"px")}i["view-params"]=i["view-params"]||{};i["view-params"].opaque=fcb;i["view-params"].skin=
i["view-params"].skin||{};fcIa(i["view-params"].skin,j);e.render(i);k={};k.id="gadget-signin";k.presentation="canvas";k.site=i.site;k.titleDivId="gfc-canvas-title";k["view-params"]={};k["view-params"].opaque=fcb;k.keepMax=i.keepMax;if(i.securityToken)k.securityToken=i.securityToken;i=fcGa(j);i.ALIGNMENT=d?"left":"right";e.Xa(k,i);h.reposition()},fcg,b,c)};fc6[fc].db=function(a,b){fc5.g!=fcc&&fc5.g.yc(a,b)};fc6[fc].Ra=function(a){fc5.g!=fcc&&fc5.g.la(a)};
fc6[fc].Ua=function(a,b,c,d,e,h,i,j,k,l){var g=this.f;a=a+(a[fcE]("?")>=0?"&":"?")+"iframeId="+g;fc5.F(a,b,c,d,e,h,i,j,k,l,this.callback)};
fc$[fc].F=function(a,b,c,d,e,h,i,j,k,l,g){var f=fcPb(fck);d!=fcc||(d=fcn[fcv](f[fcQ]*0.7));c!=fcc||(c=fcn[fcv](f[fcu]*0.7));var m=[];for(f=0;f<arguments[fct]&&f<10;f++)m[fcs](arguments[f]);if(!a[0]=="/")fca(fcf("lightbox iframes must be relative to fc server"));var n=this,o=h?fcGa(h):{},s=fcj(fcn[fcv](2147483647*fcn[fcoa]())),p="gfc_lbox_iframe_"+s;fce.rpc.setAuthToken(p,s);if(!b)b=fc5.openSocialSecurityToken;var t=fc5.openSocialSiteId;fc5.Y(function(q){n.lastIframeLightboxOpenArguments=m;var v="st="+
fci(b)+"&parent="+fci(fc5.S)+"&rpctoken="+fci(s);if(!j){o.iframeId=p;o.iurl=a;a=fch+"/friendconnect/lightbox"}var r=d-54;fcq(o,r);var u='<iframe id="'+p;u+='" width="100%" height="'+r+'" frameborder="0" scrolling="auto"></iframe>';q.setContent(u);if(e){q.setTitle(e);if(l){r=q.getTitleTextElement();fcJb(r,"lightbox-dialog-title-small-text")}}q.setVisible(fcb);k||(o.fcauth=fc5.Ja(t));a+=(a[fcE]("?")>=0?"&":"?")+v+"&communityId="+t;fcJc(p,a,"POST",o,fcc,fcc,fcc)},fcg,g,fcg,c,d)};
fc6[fc].Fa=function(){var a=fcOc(this.f);a=fc5.w(a);return a.viewParams};fc6[fc].Ea=function(){return fcDc};fc6[fc].Va=function(a,b){var c=fcOc(this.f);c=fc5.w(c);c.viewParams[a]=b};fc$[fc].Nb=function(a,b){fc5.g!=fcc&&fc5.g.Xb(b)};fc$[fc].Ob=function(a,b){fc5.g!=fcc&&fc5.g.Yb(b)};fc6[fc].Ca=function(a,b,c,d){fc5.g!=fcc&&fc5.g.rb(a,b,c,d)};fc$[fc].H=function(a){var b=this.A.Ma(a);a.render(b);this.A.postProcessGadget&&this.A.postProcessGadget(a)};
fc6[fc].signout=function(a){fc5.Wa(fc5.ea(a));fc5.Wa(fc5.ia(a));fc5.Da={};fc5.T();return fcd};fc$[fc].Wa=function(a){var b=fcl[fcC].pathname;b=b[fcz]("/");for(var c=0;c<b[fct];c++){for(var d=fcm(c+1),e=0;e<c+1;e++)d[e]=b[e];fcpb(a,d[fcS]("/")+"/")}};
fc6[fc].ab=function(a){var b=fcl[fcA](this.f);if(b&&a>0)fcq(b[fcF],a+"px");if((b=fcl[fcA](this.f+"_body"))&&a>0)fcq(b[fcF],a+"px");if(b=fcOc(this.f)){var c=fc5.w(b);if(c){if((b=fcl[fcA](c.divId))&&a>0){if(c&&c[fcta]&&c[fcta]<a){a=c[fcta];b[fcF].overflowY="auto"}fcq(b[fcF],a+"px")}!c.keepMax&&c.ka()=="canvas"&&fc5.lastLightboxDialog&&fc5.lastLightboxDialog.reposition();fc3b(c.chrome,"visibility","visible")}}};
fc6[fc].setTitle=function(a){var b=fcOc(this.f);b=fc5.w(b);if(b=b.titleDivId)fcp(fcl[fcA](b),fce[fcM].escapeString(a))};fc6[fc].signin=function(a,b,c){fcnb(fc5.ea(a),b,31104E3,c);fcnb(fc5.ia(a),b,-1,c);fc5.Da[a]=b;fc5.T()};var fcRc=function(a){fcrc(a,fcQc)};fc$[fc].ic=function(a,b){b&&this.m(b,a);var c={};c.url=fch+"/friendconnect/gadgets/members.xml";this.render(this.s(a,c))};
fc$[fc].kc=function(a,b){b&&this.m(b,a);var c={};c.url=fch+"/friendconnect/gadgets/review.xml";c["view-params"]={startMaximized:"true",disableMinMax:"true",features:"review"};this.render(this.s(a,c))};fc$[fc].ra=function(a,b){b&&this.m(b,a);var c={};c.url=fch+"/friendconnect/gadgets/wall.xml";c["view-params"]={startMaximized:"true",disableMinMax:"true",features:"comment"};this.render(this.s(a,c))};
fc$[fc].Xa=function(a,b){b&&this.m(b,a);var c={};c.url=fch+"/friendconnect/gadgets/signin.xml";fcq(c,32);this.render(this.s(a,c))};fc$[fc].fc=function(a,b){b&&this.m(b,a);a.prefs=a.prefs||{};a.sendViewParamsToServer=fcb;a.prefs.hints=fck.google_hints;var c={};c.url=fch+"/friendconnect/gadgets/ads.xml";fcq(c,90);this.render(this.s(a,c))};
fc$[fc].ua=function(a,b){if(a.id){b&&this.m(b,a);a["view-params"]=a["view-params"]||{};a["view-params"].opaque="true";this.g=new fc3(a);this.g.render();var c={};c.url=fch+"/friendconnect/gadgets/friendbar.xml";a.id=this.g.t;fcq(a,"1");this.render(this.s(a,c))}};fc$[fc].hc=fc$[fc].ua;fc$[fc].ta=function(a,b){a=a||{};a.url=fch+"/friendconnect/gadgets/signin.xml";a.site=a.site||fce[fcM][fcD]().site;fcq(a,32);this.sa(a,b)};fc$[fc].gc=fc$[fc].ta;fc$[fc].mc=fc$[fc].ra;
fc$[fc].m=function(a,b){var c=b["view-params"];if(!c){c={};b["view-params"]=c}c.skin=a};fc$[fc].s=function(a,b){var c=this.Ta(b,a);if(b["view-params"]){var d=b["view-params"];if(a["view-params"])d=this.Ta(d,a["view-params"]);c["view-params"]=d}return c};fc$[fc].jc=function(a,b){b&&this.m(b,a);this.render(a)};fc$[fc].Ta=function(a,b){var c={},d;for(d in b)c[d]=b[d];for(d in a)if(typeof c[d]=="undefined")c[d]=a[d];return c};
fc$[fc].render=function(a){this.openSocialSiteId=a.site;a["view-params"]=a["view-params"]||{};var b=this.M({divId:a.id,specUrl:a.url,communityId:a.site,height:a[fcQ],locale:a.locale||this.Wb,secureToken:a.securityToken,titleDivId:a.titleDivId,showEmbedThis:a.showEmbedThis,useLightBoxForCanvas:a.useLightBoxForCanvas||typeof a.useLightBoxForCanvas=="undefined"&&fck.friendconnect_lightbox,viewParams:a["view-params"],prefs:a.prefs,originalParams:a,debug:a.debug,maxHeight:a[fcta],sendViewParamsToServer:a.sendViewParamsToServer,
keepMax:a.keepMax});a.presentation&&b.wc(a.presentation);this.kb(b);this.A.lb(b.id,a.id);fcba(function(){fc5.H(b)},0);return b.id};fc$[fc].lc=function(a,b){a=a||{};a.presentation="canvas";this.Ya(a,b)};
fc$[fc].Ya=function(a,b,c){a=a||{};a.url=fce[fcM][fcD]().url;a.site=fce[fcM][fcD]().site||a.site;var d=fce[fcM][fcD]()["view-params"];if(d)a["view-params"]=fce[fcpa].parse(decodeURIComponent(d));if(c){a["view-params"]=a["view-params"]||{};a["view-params"].useFixedHeight=fcb;fcq(a["view-params"],c);b=b||{};b.HEIGHT=fcj(c)}this.sa(a,b)};fc$[fc].sa=function(a,b){a=a||{};b&&this.m(b,a);if(fce[fcM][fcD]().canvas=="1")a.presentation="canvas";else if(fce[fcM][fcD]().embed=="1")a.presentation="embed";fc5.render(a)};
fc$[fc].Mb=function(){var a=fce[fcM][fcD]().caller;if(a&&fcl[fcC][fcsa]!=a&&a[fct]>8&&(a.substr(0,7)[fcAa]()=="http://"||a.substr(0,8)[fcAa]()=="https://"))fcl[fcC].href=a;else if(a=fce[fcM][fcD]().site)fcl[fcC].href=fch+"/friendconnect/directory/site?id="+a;else fck.history.go(-1)};fc$[fc].G="";fc$[fc].Ib=function(){return this.G};fc$[fc].pc=function(a){this.apiVersion=a};fc$[fc].$=function(a){var b=fcl[fcK]("link");b[fcL]("rel","stylesheet");b[fcL]("type","text/css");b[fcL]("href",a);fcl.getElementsByTagName("head")[0][fcr](b)};
fc$[fc].mb=function(a){var b=fcl[fcK]("script");b[fcL]("src",a);b[fcL]("type","text/javascript");fcl.getElementsByTagName("head")[0][fcr](b)};fc$[fc].Aa=function(a){if(fcl[fcna])a();else fck[fcqa]?fck[fcqa]("load",a,fcd):fck.attachEvent("onload",a)};
fc$[fc].ma=function(a){if(!a.site)fca("API not loaded, please pass in a 'site'");this.$(fck.friendconnect_serverBase+"/friendconnect/styles/container.css?d="+this.V);this.openSocialSiteId=a.site;this.apiLoadedCallback=a.onload;this.Aa(fcW(this.Sa,this,a,"fc-opensocial-api"))};fc$[fc].Vb=fc$[fc].ma;fc$[fc].Pb=function(a){var b={};b.site=this.openSocialSiteId;b["view-params"]={txnId:a};this.Sa(b,"gfc-"+a)};
fc$[fc].ec=function(a){var b={};for(var c in this.j){var d=this.j[c];if(d.viewParams&&d.viewParams.txnId==a)break;else b[c]=d}this.j=b;(a=fcl[fcA]("gfc-"+a))&&a[fcP]&&a[fcP].removeChild&&a[fcP].removeChild(a)};fc$[fc].Cb=function(){return"<Templates xmlns:fc='http://www.google.com/friendconnect/makeThisReal'>  <Namespace prefix='fc' url='http://www.google.com/friendconnect/makeThisReal'/>  <Template tag='fc:signIn'>    <div onAttach='google.friendconnect.renderSignInButton({element: this})'></div>  </Template></Templates>"};
fc$[fc].Jb=function(){return"<Templates xmlns:os='http://ns.opensocial.org/2008/markup'><Namespace prefix='os' url='http://ns.opensocial.org/2008/markup'/><Template tag='os:Name'>  <span if='${!My.person.profileUrl}'>${My.person.displayName}</span>  <a if='${My.person.profileUrl}' href='${My.person.profileUrl}'>      ${My.person.displayName}</a></Template><Template tag='os:Badge'>  <div><img if='${My.person.thumbnailUrl}' src='${My.person.thumbnailUrl}'/>   <os:Name person='${My.person}'/></div></Template><Template tag='os:PeopleSelector'>  <select onchange='google.friendconnect.PeopleSelectorOnChange(this)' name='${My.inputName}'          multiple='${My.multiple}' x-var='${My.var}' x-max='${My.max}'          x-onselect='${My.onselect}'>    <option repeat='${My.group}' value='${Cur.id}' selected='${Cur.id == My.selected}'>        ${Cur.displayName}    </option>  </select></Template></Templates>"};
var fcSc=function(a){var b;if(a.multiple){b=[];for(var c=0;c<a[fcJ][fct];c++)a[fcJ][c].selected&&b[fcs](a[fcJ][c].value);c=a.getAttribute("x-max");try{c=1*c}catch(d){c=0}if(c&&b[fct]>c&&a["x-selected"]){b=a["x-selected"];for(c=0;c<a[fcJ][fct];c++){a[fcJ][c].selected=fcd;for(var e=0;e<b[fct];e++)if(a[fcJ][c].value==b[e]){a[fcJ][c].selected=fcb;break}}}}else b=a[fcJ][a.selectedIndex].value;a["x-selected"]=b;(c=a.getAttribute("x-var"))&&fck.opensocial[fcka]&&fck.opensocial[fcka].getDataContext().putDataSet(c,
b);if(c=a.getAttribute("x-onselect"))if(fck[c]&&typeof fck[c]=="function")fck[c](b);else if(a["x-onselect-fn"])a["x-onselect-fn"][fcN](a);else a["x-onselect-fn"]=new Function(c)};
fc$[fc].Sa=function(a,b){fck.opensocial.template.Loader.loadContent(this.Jb());fck.opensocial.template.Loader.loadContent(this.Cb());fck.opensocial[fcka].processDocumentMarkup();var c=fcl[fcK]("div");c.id=b;fcq(c[fcF],"0px");fco(c[fcF],"0px");c[fcF].position="absolute";c[fcF].visibility="hidden";fcl[fcna][fcr](c);var d={};d.url=fch+"/friendconnect/gadgets/osapi-"+this.apiVersion+".xml";fcq(d,0);d.id=c.id;d.site=a.site;d["view-params"]=a["view-params"];this.render(d)};
fc6[fc].xa=function(){fc5.G=this.f;fc5.openSocialSecurityToken=this.a[0];var a=fc5.openSocialSecurityToken;fck.opensocial[fcka].executeRequests();fck.opensocial.template.process();if(fc5.apiLoadedCallback){a=fcHa(fc5.apiLoadedCallback,a);fcba(a,0)}};fc$[fc].O=function(a){var b=fcc;for(var c in this.j)if(this.j[c].divId==a){b=this.j[c];break}return b};fc$[fc].C=function(a,b){var c=this.O(a),d=fcc;if(c)d=c.C(b);return d};fc$[fc].B=function(a,b){var c=this.O(a),d=fcc;if(c)d=c.B(b);return d};
fc$[fc].xc=function(a,b){this.Y(function(c){var d=fcl.createTextNode("Copy & paste this code into your site.");c.getContentElement()[fcr](d);c.getContentElement()[fcr](fcl[fcK]("br"));d=fc5.B(a,b);var e=fcl[fcK]("textarea");fcp(e,d);e[fcL]("style","width:500px;");c.getContentElement()[fcr](e);c.setVisible(fcb)})};
var fcTc=["ar","dv","fa","iw","he","ku","pa","sd","tk","ug","ur","yi"],fcPc=function(a){a=a;var b=fcd;if(a){a=a[fcz]("_")[0];b=fcxb(fcTc,a)}else b=(a=fc5b(fcl[fcna],"direction"))&&a=="rtl";return b};fc6[fc].fb=function(a,b){var c=0,d=fcc;try{var e=fcOc(this.f),h=fc5.w(e);d=h.secureToken;c=h.communityId}catch(i){}if(b)c=b;fc5.I(a,c,this.callback,d)};
fc$[fc].I=function(a,b,c,d){b=b||this.openSocialSiteId;a={keepMax:fcb,presentation:"canvas",url:fch+"/friendconnect/gadgets/members.xml",site:b,"view-params":{profileId:a}};if(d)a.securityToken=d;this.eb(a,c)};fc$[fc].Eb=function(a){var b=fcc;if((a=this.O(a))&&a.secureToken)b=a.secureToken;return b};fc$[fc].Db=function(a){var b=fcc;if((a=this.O(a))&&a.communityId)b=a.communityId;return b};
var fcQc=function(a){fc5.G&&fclc(fc5.G,a)},fcUc=function(){fc6[fc].signout(fc5.openSocialSiteId)},fcVc=function(){fcoc(fc5.G)},fcWc=function(a,b){fcic(a,b)},fcxc=function(){this.o={}};fcxc[fc].register=function(){fce.rpc[fcR]("subscribeEventType",fc6[fc].subscribe);fce.rpc[fcR]("publishEvent",fc6[fc].publish)};fc6[fc].subscribe=function(a){var b=fcMc;b.o[a]=b.o[a]||[];a=b.o[a];a[a[fct]]={frameId:this}};fcxc[fc].gb=function(a,b,c){var d=this;d.o[b]=d.o[b]||[];b=d.o[b];b[b[fct]]={container:a,callback:c}};
fc6[fc].publish=function(a){var b=fcMc,c=0;if(this.f)c=fcOc(this.f);b.o[a]=b.o[a]||[];b=b.o[a];for(var d=0;d<b[fct];d++)b[d].container?b[d].callback[fcH](b[d].container,a,c):fce.rpc[fcH](b[d].frameId,a,fcc,a,c)};var fcyc=fcW(fc6[fc].publish,new fc6),fcMc=new fcxc,fc5=new fc$;fc5.Aa(fc5.vb);fcX("google.friendconnect.container",fc5);fcX("google.friendconnect.container.refreshGadgets",fc5.T);fcX("google.friendconnect.container.setParentUrl",fc5.W);fcX("google.friendconnect.container.setServerBase",fc5.X);
fcX("google.friendconnect.container.setServerVersion",fc5.vc);fcX("google.friendconnect.container.createGadget",fc5.M);fcX("google.friendconnect.container.openLightboxIframe",fc5.F);fcX("google.friendconnect.container.renderGadget",fc5.H);fcX("google.friendconnect.container.render",fc5.render);fcX("google.friendconnect.container.goBackToSite",fc5.Mb);fcX("google.friendconnect.container.renderMembersGadget",fc5.ic);fcX("google.friendconnect.container.renderReviewGadget",fc5.kc);
fcX("google.friendconnect.container.renderCommentsGadget",fc5.ra);fcX("google.friendconnect.container.renderSignInGadget",fc5.Xa);fcX("google.friendconnect.container.renderFriendBar",fc5.hc);fcX("google.friendconnect.container.renderSocialBar",fc5.ua);fcX("google.friendconnect.container.renderCanvasSignInGadget",fc5.gc);fcX("google.friendconnect.container.renderUrlCanvasGadget",fc5.lc);fcX("google.friendconnect.container.renderEmbedSignInGadget",fc5.ta);
fcX("google.friendconnect.container.renderUrlEmbedGadget",fc5.Ya);fcX("google.friendconnect.container.renderEmbedGadget",fc5.sa);fcX("google.friendconnect.container.renderWallGadget",fc5.mc);fcX("google.friendconnect.container.renderAdsGadget",fc5.fc);fcX("google.friendconnect.container.renderOpenSocialGadget",fc5.jc);fcX("google.friendconnect.container.setNoCache",fc5.bb);fcX("google.friendconnect.container.enableProxy",fc5.Ga);fcX("google.friendconnect.container.setDomain",fc5.rc);
fcX("google.friendconnect.container.setLockedDomainSuffix",fc5.uc);fcX("google.friendconnect.container.setLocale",fc5.tc);fcX("google.friendconnect.container.loadOpenSocialApi",fc5.Vb);fcX("google.friendconnect.container.initOpenSocialApi",fc5.ma);fcX("google.friendconnect.container.getOpenSocialApiIframeId",fc5.Ib);fcX("google.friendconnect.container.setApiVersion",fc5.pc);fcX("google.friendconnect.container.getEmbedUrl",fc5.C);fcX("google.friendconnect.container.getEmbedHtml",fc5.B);
fcX("google.friendconnect.container.getGadgetSecurityToken",fc5.Eb);fcX("google.friendconnect.container.getGadgetCommunityId",fc5.Db);fcX("google.friendconnect.container.showEmbedDialog",fc5.xc);fcX("google.friendconnect.container.showMemberProfile",fc5.I);fcX("google.friendconnect.requestSignIn",fcQc);fcX("google.friendconnect.requestSignOut",fcUc);fcX("google.friendconnect.requestSettings",fcVc);fcX("google.friendconnect.requestInvite",fcWc);fcX("google.friendconnect.renderSignInButton",fcRc);
fcX("google.friendconnect.container.invokeOpenSocialApiViaIframe",fc5.Pb);fcX("google.friendconnect.container.removeOpenSocialApiViaIframe",fc5.ec);fcX("google.friendconnect.userAgent.WEBKIT",fcdb);fcX("google.friendconnect.userAgent.IE",fcZ);fcX("google.friendconnect.PeopleSelectorOnChange",fcSc);fcX("google.friendconnect.container.setDateStamp_",fc5.qc);
google.friendconnect.container.setServerBase('http://www.a.friendconnect.gmodules.com/ps/');google.friendconnect.container.setServerVersion('0.548.6');google.friendconnect.container.setApiVersion('0.8');
google.friendconnect.container.setDomain('http://www.google.com/friendconnect/gadgets/activities.xml', 'http://q8j0igk2u2f6kf7jogh6s66md2d7r154.a.friendconnect.gmodules.com/ps/');

google.friendconnect.container.setDomain('http://www.google.com/friendconnect/gadgets/ads.xml', 'http://t767uouk8skpac15v8ue0n16regb3m2t.a.friendconnect.gmodules.com/ps/');

google.friendconnect.container.setDomain('http://www.google.com/friendconnect/gadgets/ask.xml', 'http://uofgf6lm45rimd9jp6hn983ul6n2en81.a.friendconnect.gmodules.com/ps/');

google.friendconnect.container.setDomain('http://www.google.com/friendconnect/gadgets/friendbar.xml', 'http://p7rjrrl49ose4gob99eonlvp0drmce3d.a.friendconnect.gmodules.com/ps/');

google.friendconnect.container.setDomain('http://www.google.com/friendconnect/gadgets/content_reveal.xml', 'http://n0mc7q283f00tpk3uifa7sjv4hmrults.a.friendconnect.gmodules.com/ps/');

google.friendconnect.container.setDomain('http://www.google.com/friendconnect/gadgets/chat.xml', 'http://4mmefl67as0q39gf1o4pnocubqmdgei0.a.friendconnect.gmodules.com/ps/');

google.friendconnect.container.setDomain('http://www.google.com/friendconnect/gadgets/donate.xml', 'http://7v4nflqvq38notsghmcr5a9t6o9g6kn4.a.friendconnect.gmodules.com/ps/');

google.friendconnect.container.setDomain('http://www.google.com/friendconnect/gadgets/lamegame.xml', 'http://ffbrstu9puk7qmt45got9mqe5k7ijrs4.a.friendconnect.gmodules.com/ps/');

google.friendconnect.container.setDomain('http://www.google.com/friendconnect/gadgets/map.xml', 'http://k0dfp8trn0hi5d2spmo7jmc88n6kr1cc.a.friendconnect.gmodules.com/ps/');

google.friendconnect.container.setDomain('http://www.google.com/friendconnect/gadgets/members.xml', 'http://r1rk9np7bpcsfoeekl0khkd2juj27q3o.a.friendconnect.gmodules.com/ps/');

google.friendconnect.container.setDomain('http://www.google.com/friendconnect/gadgets/newsletterSubscribe.xml', 'http://k830suiki828goudg9448o6bp0tpu5r3.a.friendconnect.gmodules.com/ps/');

google.friendconnect.container.setDomain('http://www.google.com/friendconnect/gadgets/poll.xml', 'http://1ivjd75aqp679vbgohjv74tlhn13rgdu.a.friendconnect.gmodules.com/ps/');

google.friendconnect.container.setDomain('http://www.google.com/friendconnect/gadgets/recommended_pages.xml', 'http://iqavu79a908u5vcecp0pq80hhbhkv33b.a.friendconnect.gmodules.com/ps/');

google.friendconnect.container.setDomain('http://www.google.com/friendconnect/gadgets/review.xml', 'http://r85jiaoot111joesr8bilfhfeslcc496.a.friendconnect.gmodules.com/ps/');

google.friendconnect.container.setDomain('http://www.google.com/friendconnect/gadgets/sample.xml', 'http://785aoao97uti9iqffknjp5e0kn2ljlm4.a.friendconnect.gmodules.com/ps/');

google.friendconnect.container.setDomain('http://www.google.com/friendconnect/gadgets/signin.xml', 'http://8fkcem1ves287v3g5lu9gep1j91p3kk1.a.friendconnect.gmodules.com/ps/');

google.friendconnect.container.setDomain('http://www.google.com/friendconnect/gadgets/wall.xml', 'http://o29lt44ell30t7ljcdfr8lq2mjakv2co.a.friendconnect.gmodules.com/ps/');

google.friendconnect.container.setDomain('http://www.google.com/friendconnect/gadgets/osapi-0.8.xml', 'http://mc8tdi0ripmbpds25eboaupdulritrp6.a.friendconnect.gmodules.com/ps/');

google.friendconnect.container.setLockedDomainSuffix('.a.friendconnect.gmodules.com/ps/');
window['__ps_loaded__'] = true; 
 }google.friendconnect_ = google.friendconnect;
google.friendconnect.container.setDateStamp_('12a4cfa6b58');