// (function( $ ) {
//     "use strict";
//     $(function() {
//         function animated_contents() {
//             $(".zt-skill-bar > div ").each(function (i) {
//                 var $this  = $(this),
//                     skills = $this.data('width');
 
//                 $this.css({'width' : skills + '%'});
 
//             });
//         }
        
//         if(jQuery().appear) {
//             $('.zt-skill-bar').appear().on('appear', function() {
//                 animated_contents();
//             });
//         } else {
//             animated_contents();
//         }
//     });
// }(jQuery));

let t = 0
bar.style.width = 0
const barAnimation = setInterval(() => {
  bar.style.width =  t + '%'
  t++ >= totalMinwon && clearInterval(barAnimation)
}, 10)

// let t4 = 0
// const donut = document.querySelector(".donut")
// const donutAnimation = setInterval(() => {
//   donut.dataset.percent = t4
//   donut.style.background = `conic-gradient(#4F98FF 0 ${t4}%, #DEDEDE ${t4}% 100% )`
//   t4++ >= totalMinwon && clearInterval(donutAnimation)
// }, 10)