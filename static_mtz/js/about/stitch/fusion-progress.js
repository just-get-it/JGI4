!function(r){"use strict";r.fn.fusion_draw_progress=function(){r(this).find(".progress").css("width",function(){return r(this).attr("aria-valuenow")+"%"})}}(jQuery),jQuery(document).ready(function(){jQuery(".fusion-progressbar").not(".fusion-modal .fusion-progressbar").each(function(){var r=getWaypointOffset(jQuery(this));jQuery(this).waypoint(function(){jQuery(this).fusion_draw_progress()},{triggerOnce:!0,offset:r})})}),jQuery(window).load(function(){jQuery(".fusion-modal .fusion-progressbar").on("appear",function(){jQuery(this).fusion_draw_progress()})}),jQuery(window).on("fusion-element-render-fusion_progress",function(r,n){(void 0!==n?jQuery('div[data-cid="'+n+'"]').find(".fusion-progressbar"):jQuery(".fusion-progressbar")).fusion_draw_progress()});