function avadaLightBoxInitializeLightbox(){
    var t;
    if(window.$ilInstances)
        for(t=0;t<window.$ilInstances.length;t++)
            window.$ilInstances[t].destroy();
            window.avadaLightBox.initialize_lightbox()
}
window.avadaLightBox={},
void 0===window.$ilInstances&&(window.$ilInstances=[]),window.avadaLightBox.initialize_lightbox=function(){
    "use strict";
    1===Number(fusionLightboxVars.status_lightbox)&&(window.avadaLightBox.set_title_and_caption(),
    window.avadaLightBox.activate_lightbox())
},
window.avadaLightBox.activate_lightbox=function(t){
    "use strict";
    var i,o=[];
    void 0===t&&(t=jQuery("body")),
    t.find('[data-rel^="prettyPhoto["], [rel^="prettyPhoto["], [data-rel^="iLightbox["], [rel^="iLightbox["]').each(function(){
        var t,
        i,
        a,
        e,
        n=["bmp","gif","jpeg","jpg","png","tiff","tif","jfif","jpe","svg","mp4","ogg","webm"],
        r=0,
        s=jQuery(this).attr("href");
        for(void 0===s&&(s=""),t=0;t<n.length;t++)
            r+=String(s).toLowerCase().indexOf("."+n[t]);
            i=/http(s?):\/\/(www\.)?vimeo.com\/(\d+)/,
            s.match(i)&&(r=1),
            i=/^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#\&\?]*).*/,
            s.match(i)&&(r=1),
            -13===parseInt(r,10)&&(jQuery(this).addClass("fusion-no-lightbox"),
            jQuery(this).removeAttr("data-rel rel")),
            jQuery(this).hasClass("fusion-no-lightbox")||(null!=(a=this.getAttribute("data-rel"))&&-1===jQuery.inArray(a,o)&&o.push(a),
            null!=(e=this.getAttribute("data-rel"))&&(jQuery(this).parents(".gallery").length&&(e=e.replace("postimages",jQuery(this).parents(".gallery").attr("id")),
            jQuery(this).attr("data-rel",e)),-1===jQuery.inArray(e,o)&&o.push(e)))
        }),
        i=1,t.find(".tiled-gallery").each(function(){
            jQuery(this).find(".tiled-gallery-item > a").each(function(){
                var t=this.getAttribute("data-rel");
                null==t&&(t="iLightbox[tiled-gallery-"+i+"]",jQuery(this).attr("data-rel",t)),
                -1===jQuery.inArray(t,o)&&o.push(t)
            }),
            i++
        }),
        jQuery.each(o,function(t,i){
            1===jQuery('[data-rel="'+i+'"], [rel="'+i+'"]').length?window.$ilInstances.push(jQuery('[data-rel="'+i+'"], [rel="'+i+'"]').iLightBox(window.avadaLightBox.prepare_options(i,!1))):window.$ilInstances.push(jQuery('[data-rel="'+i+'"], [rel="'+i+'"]').iLightBox(window.avadaLightBox.prepare_options(i)))
        }),
        t.find('a[rel="prettyPhoto"], a[data-rel="prettyPhoto"], a[rel="iLightbox"], a[data-rel="iLightbox"]').each(function(){
            var t=jQuery(this).attr("href");
            ""!==t&&void 0!==t&&window.$ilInstances.push(jQuery(this).iLightBox(window.avadaLightBox.prepare_options("single")))
        }),
        t.find("#lightbox-link, .lightbox-link, .fusion-lightbox-link").each(function(){
            var t=jQuery(this).attr("href");
            ""!==t&&void 0!==t&&window.$ilInstances.push(jQuery(this).iLightBox(window.avadaLightBox.prepare_options("single")))
        }),
        fusionLightboxVars.lightbox_post_images&&t.find(".type-post .post-content a, #posts-container .post .post-content a, .fusion-blog-shortcode .post .post-content a, .type-avada_portfolio .project-content a, .fusion-portfolio .fusion-portfolio-wrapper .fusion-post-content, .summary-container .post-content a, .woocommerce-tabs .post-content a").has("img").each(function(){var t,i=["bmp","gif","jpeg","jpg","png","tiff","tif","jfif","jpe","svg","mp4","ogg","webm"],o=0;for(t=0;t<i.length;t++)o+=String(jQuery(this).attr("href")).toLowerCase().indexOf("."+i[t]);-13===parseInt(o,10)&&(jQuery(this).addClass("fusion-no-lightbox"),jQuery(this).removeAttr("data-rel rel")),-1!==String(jQuery(this).attr("rel")).indexOf("prettyPhoto")||-1!==String(jQuery(this).attr("data-rel")).indexOf("prettyPhoto")||-1!==String(jQuery(this).attr("rel")).indexOf("iLightbox")||-1!==String(jQuery(this).attr("data-rel")).indexOf("iLightbox")||jQuery(this).hasClass("fusion-no-lightbox")||(jQuery(this).attr("data-caption",jQuery(this).parent().find("p.wp-caption-text").text()),window.$ilInstances.push(jQuery(this).iLightBox(window.avadaLightBox.prepare_options("post"))))})},window.avadaLightBox.set_title_and_caption=function(){"use strict";jQuery('a[rel^="prettyPhoto"], a[data-rel^="prettyPhoto"]').each(function(){jQuery(this).attr("data-caption")||(jQuery(this).attr("title")?jQuery(this).attr("data-caption",jQuery(this).attr("title")):jQuery(this).attr("data-caption",jQuery(this).parents(".gallery-item").find(".gallery-caption").text())),jQuery(this).attr("data-title")||jQuery(this).attr("data-title",jQuery(this).find("img").attr("alt"))}),jQuery('a[rel^="iLightbox"], a[data-rel^="iLightbox"]').each(function(){jQuery(this).attr("data-caption")||jQuery(this).attr("data-caption",jQuery(this).parents(".gallery-item").find(".gallery-caption").text())})},window.avadaLightBox.prepare_options=function(t,i){"use strict";var o,a,e=!0;return void 0===i&&(i=fusionLightboxVars.lightbox_gallery,e=!(!0===fusionLightboxVars.lightbox_autoplay||"true"===fusionLightboxVars.lightbox_autoplay||1===fusionLightboxVars.lightbox_autoplay||"1"===fusionLightboxVars.lightbox_autoplay)),o={fast:100,slow:800,normal:400},a={skin:fusionLightboxVars.lightbox_skin,smartRecognition:!1,minScale:.075,show:{title:fusionLightboxVars.lightbox_title,speed:o[fusionLightboxVars.lightbox_animation_speed.toLowerCase()]},path:fusionLightboxVars.lightbox_path,controls:{slideshow:i,arrows:fusionLightboxVars.lightbox_arrows},slideshow:{pauseTime:fusionLightboxVars.lightbox_slideshow_speed,pauseOnHover:!1,startPaused:e},overlay:{opacity:fusionLightboxVars.lightbox_opacity},caption:{start:fusionLightboxVars.lightbox_desc,show:"",hide:""},isMobile:!0,callback:{onShow:function(t,i){var o=jQuery(t.currentElement).find('iframe[src*="youtube.com"]');jQuery('.ilightbox-container iframe[src*="youtube.com"]').not(o).each(function(){this.contentWindow.postMessage('{"event":"command","func":"pauseVideo","args":""}',"*")})},onAfterChange:function(t){var i=jQuery(t.currentElement).find('iframe[src*="youtube.com"]'),o=i.length?i.attr("src"):"";jQuery('.ilightbox-container iframe[src*="youtube.com"]').not(i).each(function(){this.contentWindow.postMessage('{"event":"command","func":"pauseVideo","args":""}',"*")}),i.length&&-1!==o.indexOf("autoplay=1")&&i[0].contentWindow.postMessage('{"event":"command","func":"playVideo","args":""}',"*")}}},fusionLightboxVars.lightbox_social&&(a.social={buttons:{facebook:!0,twitter:!0,reddit:!0,digg:!0,delicious:!0}}),Number(fusionLightboxVars.lightbox_deeplinking)&&(a.linkId=t),a},window.avadaLightBox.refresh_lightbox=function(){"use strict";window.avadaLightBox.set_title_and_caption(),jQuery.each(window.$ilInstances,function(t,i){i.hasOwnProperty("refresh")&&i.refresh()})},void 0===window.$ilInstances&&(window.$ilInstances=[]),jQuery(document).ajaxComplete(function(){"use strict";window.avadaLightBox.refresh_lightbox()}),jQuery(window).load(function(){"use strict";window.avadaLightBox.initialize_lightbox()});