(this["webpackJsonpgogo-react"]=this["webpackJsonpgogo-react"]||[]).push([[3],{106:function(e,t,n){"use strict";n.d(t,"a",(function(){return i}));var a=n(16),c=n.n(a),r=n(90),s=n(6),o=function(e){return{type:s.m,payload:e}},i=function(){return function(){var e=Object(r.a)(c.a.mark((function e(t){var n,a;return c.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return t({type:s.c}),e.prev=1,e.next=4,fetch("/api/actress_detail");case 4:return n=e.sent,e.next=7,n.json();case 7:a=e.sent,t((r=a,{type:s.d,payload:r})),t(o(a)),e.next=15;break;case 12:e.prev=12,e.t0=e.catch(1),t((c=e.t0.message,{type:s.b,payload:c}));case 15:case"end":return e.stop()}var c,r}),e,null,[[1,12]])})));return function(t){return e.apply(this,arguments)}}()}},128:function(e,t){e.exports={"general.copyright":"Gogo React \xa9 2018 All Rights Reserved.","user.login-title":"Login","user.register":"Register","user.forgot-password":"Forgot Password","user.email":"E-mail","user.password":"Password","user.forgot-password-question":"Forget password?","user.fullname":"Full Name","user.login-button":"LOGIN","user.register-button":"REGISTER","user.reset-password-button":"RESET","user.buy":"BUY","user.username":"Username","menu.home":"Home","menu.app":"Home","menu.dashboards":"Dashboards","menu.gogo":"Gogo","menu.start":"Start","menu.second-menu":"Second Menu","menu.second":"Second","menu.ui":"UI","menu.charts":"Charts","menu.chat":"Chat","menu.survey":"Survey","menu.todo":"Todo","menu.search":"Search","menu.docs":"Docs","menu.blank-page":"Blank Page","pages.error-title":"Ooops... looks like an error occurred!","pages.error-code":"Error code","pages.go-back-home":"GO BACK HOME"}},168:function(e,t){e.exports={"general.copyright":"Gogo React \xa9 Todos los derechos reservados.","user.login-title":"Iniciar sesi\xf3n","user.register":"Registro","user.forgot-password":"Se te olvid\xf3 tu contrase\xf1a","user.email":"Email","user.password":"Contrase\xf1a","user.forgot-password-question":"\xbfContrase\xf1a olvidada?","user.fullname":"Nombre completo","user.login-button":"INICIAR SESI\xd3N","user.register-button":"REGISTRO","user.reset-password-button":"REINICIAR","user.buy":"COMPRAR","user.username":"Nombre de Usuario","menu.home":"Inicio","menu.app":"Inicio","menu.dashboards":"Tableros","menu.gogo":"Gogo","menu.start":"Comienzo","menu.second-menu":"Segundo men\xfa","menu.second":"Segundo","menu.ui":"IU","menu.charts":"Gr\xe1ficos","menu.chat":"Chatea","menu.survey":"Encuesta","menu.todo":"Notas","menu.search":"B\xfasqueda","menu.docs":"Docs","menu.blank-page":"Blank Page","layouts.error-title":"Vaya, parece que ha ocurrido un error!","layouts.error-code":"C\xf3digo de error","layouts.go-back-home":"REGRESAR A INICIO"}},298:function(e,t,n){"use strict";n.r(t);var a=n(4),c=n(16),r=n.n(c),s=n(90),o=n(91),i=n(92),u=n(96),l=n(95),d=n(2),m=n.n(d),h=n(20),f=n(69),j=n(72),b=n(299),p=n(106),O=n(6),v=function(e){return{type:O.n,payload:e}},g=n(128),x=n.n(g),y={messages:Object(a.a)({},x.a),locale:"en-US"},k=n(168),C=n.n(k),N={en:y,es:{messages:Object(a.a)({},C.a),locale:"es-ES"},enrtl:{messages:Object(a.a)({},x.a),locale:"en-US"}},R=n(70),w=n(268),S=n(269),E=n(302),I=n(11),T=n(5),L=n(10),q=function(){var e=Object(d.useRef)(),t=Object(d.useState)(!1),n=Object(R.a)(t,2),a=n[0],c=n[1],r=Object(d.useState)(Object(I.a)()),s=Object(R.a)(r,1)[0],o=Object(d.useState)(Object(I.c)()),i=Object(R.a)(o,2),u=i[0],l=i[1];Object(d.useEffect)((function(){"flat"===u?document.body.classList.remove("rounded"):document.body.classList.add("rounded"),Object(I.g)(u),a&&c(!1)}),[u]);var m=function(t){if(a){var n=e.current;if(n.contains(t.target)||n===t.target)return;c(!1)}};Object(d.useEffect)((function(){return["click","touchstart"].forEach((function(e){return document.addEventListener(e,m,!1)})),function(){["click","touchstart"].forEach((function(e){return document.removeEventListener(e,m,!1)}))}}),[a]);var h=function(e,t){e.preventDefault(),Object(I.e)(t),c(!1),setTimeout((function(){window.location.reload()}),500)};return Object(L.jsxs)("div",{ref:e,className:"theme-colors ".concat(a?"shown":""),children:[Object(L.jsxs)("div",{className:"p-4",children:[Object(L.jsx)("p",{className:"text-muted mb-2",children:"Light Theme"}),Object(L.jsx)("div",{className:"d-flex flex-row justify-content-between mb-3",children:T.b.slice(0,5).map((function(e){return Object(L.jsx)("a",{href:"#light.".concat(e),className:"theme-color theme-color-".concat(e," ").concat(s==="light.".concat(e)?"active":""),onClick:function(t){return h(t,"light.".concat(e))},children:Object(L.jsx)("span",{children:" "})},"light.".concat(e))}))}),Object(L.jsx)("div",{className:"d-flex flex-row justify-content-between mb-4",children:T.b.slice(5,10).map((function(e){return Object(L.jsx)("a",{href:"#light.".concat(e),className:"theme-color theme-color-".concat(e," ").concat(s==="light.".concat(e)?"active":""),onClick:function(t){return h(t,"light.".concat(e))},children:Object(L.jsx)("span",{children:" "})},"light.".concat(e))}))}),Object(L.jsx)("p",{className:"text-muted mb-2",children:"Dark Theme"}),Object(L.jsx)("div",{className:"d-flex flex-row justify-content-between mb-3",children:T.b.slice(0,5).map((function(e){return Object(L.jsx)("a",{href:"#dark.".concat(e),className:"theme-color theme-color-".concat(e," ").concat(s==="dark.".concat(e)?"active":""),onClick:function(t){return h(t,"dark.".concat(e))},children:Object(L.jsx)("span",{children:" "})},"dark.".concat(e))}))}),Object(L.jsx)("div",{className:"d-flex flex-row justify-content-between",children:T.b.slice(5,10).map((function(e){return Object(L.jsx)("a",{href:"#dark.".concat(e),className:"theme-color theme-color-".concat(e," ").concat(s==="dark.".concat(e)?"active":""),onClick:function(t){return h(t,"dark.".concat(e))},children:Object(L.jsx)("span",{children:" "})},"dark.".concat(e))}))})]}),Object(L.jsx)("div",{className:" pb-0 pl-4 pt-4",children:Object(L.jsxs)(w.a,{children:[Object(L.jsx)(S.a,{for:"radiusRadio",children:"Border Radius "}),Object(L.jsxs)("div",{children:[Object(L.jsx)(E.a,{type:"radio",name:"radiusRadio",id:"rounded",label:"Rounded",inline:!0,defaultChecked:"rounded"===u,onChange:function(){return l("rounded")}}),Object(L.jsx)(E.a,{type:"radio",name:"radiusRadio",id:"flat",label:"Flat",inline:!0,defaultChecked:"flat"===u,onChange:function(){return l("flat")}})]})]})}),Object(L.jsxs)("a",{href:"#section",className:"theme-button",onClick:function(e){e.preventDefault(),c(!a)},children:[" ",Object(L.jsx)("i",{className:"simple-icon-magic-wand"})," "]})]})},H=n(304),F=n(300),A=n(66),G=n.n(A),P=function(e){var t=e.title,n=e.type,a=e.message,c=e.customClassName,r=e.timeOut,s=e.onClick,o=e.onRequestHide,i=function(){o&&o()};Object(d.useEffect)((function(){var e=null;return 0!==r&&(e=setTimeout(i,r)),function(){e&&clearTimeout(e)}}),[]);var u=function(){s&&s(),i()},l=G()(["notification","notification-".concat(n),c]),m=t?Object(L.jsx)("h4",{className:"title",children:t}):null;return Object(L.jsx)("div",{className:l,onClick:function(){return u()},children:Object(L.jsxs)("div",{className:"notification-message",role:"alert",children:[m,Object(L.jsx)("div",{className:"message",children:a})]})})};P.defaultProps={type:"info",title:null,message:null,timeOut:5e3,onClick:function(){},onRequestHide:function(){},customClassName:""};var U=P,D=function(e){Object(u.a)(n,e);var t=Object(l.a)(n);function n(){var e;Object(o.a)(this,n);for(var a=arguments.length,c=new Array(a),r=0;r<a;r++)c[r]=arguments[r];return(e=t.call.apply(t,[this].concat(c))).handleRequestHide=function(t){return function(){var n=e.props.onRequestHide;n&&n(t)}},e}return Object(i.a)(n,[{key:"render",value:function(){var e=this,t=this.props,n=t.notifications,a=t.enterTimeout,c=t.leaveTimeout,r=G()("notification-container",{"notification-container-empty":0===n.length});return Object(L.jsx)("div",{className:r,children:Object(L.jsx)(H.a,{children:n.map((function(t){var n=t.id||(new Date).getTime();return Object(L.jsx)(F.a,{classNames:"notification",timeout:{exit:c,enter:a},children:Object(L.jsx)(U,{type:t.type,title:t.title,message:t.message,timeOut:t.timeOut,onClick:t.onClick,onRequestHide:e.handleRequestHide(t),customClassName:t.customClassName},n)},n)}))})})}}]),n}(m.a.Component);D.defaultProps={notifications:[],onRequestHide:function(){},enterTimeout:400,leaveTimeout:400};var B=D,M=n(169),z="change",J="primary",W="secondary",K="info",V="success",Y="warning",_="error",Q=new(function(e){Object(u.a)(n,e);var t=Object(l.a)(n);function n(){var e;return Object(o.a)(this,n),(e=t.call(this)).listNotify=[],e}return Object(i.a)(n,[{key:"create",value:function(e){var t={id:"xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g,(function(e){var t=16*Math.random()|0;return("x"===e?t:3&t|8).toString(16)})),type:"info",title:null,message:null,timeOut:5e3,customClassName:""};e.priority?this.listNotify.unshift(Object.assign(t,e)):this.listNotify.push(Object.assign(t,e)),this.emitChange()}},{key:"primary",value:function(e,t,n,a,c,r){this.create({type:J,message:e,title:t,timeOut:n,onClick:a,priority:c,customClassName:r})}},{key:"secondary",value:function(e,t,n,a,c,r){this.create({type:W,message:e,title:t,timeOut:n,onClick:a,priority:c,customClassName:r})}},{key:"info",value:function(e,t,n,a,c,r){this.create({type:K,message:e,title:t,timeOut:n,onClick:a,priority:c,customClassName:r})}},{key:"success",value:function(e,t,n,a,c,r){this.create({type:V,message:e,title:t,timeOut:n,onClick:a,priority:c,customClassName:r})}},{key:"warning",value:function(e,t,n,a,c,r){this.create({type:Y,message:e,title:t,timeOut:n,onClick:a,priority:c,customClassName:r})}},{key:"error",value:function(e,t,n,a,c,r){this.create({type:_,message:e,title:t,timeOut:n,onClick:a,priority:c,customClassName:r})}},{key:"remove",value:function(e){this.listNotify=this.listNotify.filter((function(t){return e.id!==t.id})),this.emitChange()}},{key:"emitChange",value:function(){this.emit(z,this.listNotify)}},{key:"addChangeListener",value:function(e){this.addListener(z,e)}},{key:"removeChangeListener",value:function(e){this.removeListener(z,e)}}]),n}(M.EventEmitter)),X=function(e){Object(u.a)(n,e);var t=Object(l.a)(n);function n(e){var a;return Object(o.a)(this,n),(a=t.call(this,e)).componentWillUnmount=function(){Q.removeChangeListener(a.handleStoreChange)},a.handleStoreChange=function(e){a.setState({notifications:e})},a.handleRequestHide=function(e){Q.remove(e)},Q.addChangeListener(a.handleStoreChange),a.state={notifications:[]},a}return Object(i.a)(n,[{key:"render",value:function(){var e=this.state.notifications,t=this.props,n=t.enterTimeout,a=t.leaveTimeout;return Object(L.jsx)(B,{enterTimeout:n,leaveTimeout:a,notifications:e,onRequestHide:this.handleRequestHide})}}]),n}(m.a.Component);X.defaultProps={enterTimeout:400,leaveTimeout:400};var Z=X,$=m.a.lazy((function(){return Promise.all([n.e(13),n.e(9)]).then(n.bind(null,297))})),ee=m.a.lazy((function(){return n.e(10).then(n.bind(null,280))})),te=function(e){Object(u.a)(n,e);var t=Object(l.a)(n);function n(e){var a;Object(o.a)(this,n),a=t.call(this,e);return Object(I.d)().isRtl?(document.body.classList.add("rtl"),document.body.classList.remove("ltr")):(document.body.classList.add("ltr"),document.body.classList.remove("rtl")),a}return Object(i.a)(n,[{key:"componentDidMount",value:function(){var e=this.props,t=e.FetchActresses,n=e.FetchFilms;t(),n();var a=setInterval(Object(s.a)(r.a.mark((function e(){return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:document.hasFocus()&&(t(),n());case 1:case"end":return e.stop()}}),e)}))),1e3);this.intervalId=a}},{key:"componentWillUnmount",value:function(){clearInterval(this.intervalId)}},{key:"render",value:function(){var e=this.props.locale,t=N[e];return Object(L.jsx)("div",{className:"h-100",children:Object(L.jsx)(b.a,{locale:t.locale,messages:t.messages,children:Object(L.jsxs)(L.Fragment,{children:[Object(L.jsx)(Z,{}),T.h&&Object(L.jsx)(q,{}),Object(L.jsx)(d.Suspense,{fallback:Object(L.jsx)("div",{className:"loading"}),children:Object(L.jsx)(f.a,{children:Object(L.jsxs)(j.Switch,{children:[Object(L.jsx)(j.Route,{path:T.a,render:function(e){return Object(L.jsx)($,Object(a.a)({},e))}}),Object(L.jsx)(j.Route,{path:"/error",exact:!0,render:function(e){return Object(L.jsx)(ee,Object(a.a)({},e))}}),Object(L.jsx)(j.Redirect,{exact:!0,from:"/",to:"".concat(T.a,"/accueil")}),Object(L.jsx)(j.Redirect,{to:"/error"}),Object(L.jsx)(j.Redirect,{to:"/error"})]})})})]})})})}}]),n}(m.a.Component);t.default=Object(h.b)((function(e){return{locale:e.settings.locale}}),(function(e){return{FetchActresses:function(){return e(Object(p.a)())},FetchFilms:function(){return e(function(){var e=Object(s.a)(r.a.mark((function e(t){var n,a;return r.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return t({type:O.f}),e.prev=1,e.next=4,fetch("/api/films");case 4:return n=e.sent,e.next=7,n.json();case 7:a=e.sent,t((r=a,{type:O.g,payload:r})),t(v(a)),e.next=15;break;case 12:e.prev=12,e.t0=e.catch(1),t((c=e.t0.message,{type:O.e,payload:c}));case 15:case"end":return e.stop()}var c,r}),e,null,[[1,12]])})));return function(t){return e.apply(this,arguments)}}())}}}))(te)}}]);