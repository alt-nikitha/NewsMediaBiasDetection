// /**
// * Template Name: Siimple - v2.1.0
// * Template URL: https://bootstrapmade.com/free-bootstrap-landing-page/
// * Author: BootstrapMade.com
// * License: https://bootstrapmade.com/license/
// */
// !(function($) {
//   "use strict";

//   // Toggle nav menu
//   $(document).on('click', '.nav-toggle', function(e) {
//     $('.nav-menu').toggleClass('nav-menu-active');
//     $('.nav-toggle').toggleClass('nav-toggle-active');
//     $('.nav-toggle i').toggleClass('bx-x bx-menu');

//   });

//   // Toogle nav menu drop-down items
//   $(document).on('click', '.nav-menu .drop-down > a', function(e) {
//     e.preventDefault();
//     $(this).next().slideToggle(300);
//     $(this).parent().toggleClass('active');
//   });

//   // Smooth scroll for the navigation menu and links with .scrollto classes
//   $(document).on('click', '.nav-menu a, .scrollto', function(e) {
//     if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
//       e.preventDefault();
//       var target = $(this.hash);
//       if (target.length) {

//         var scrollto = target.offset().top;

//         if ($(this).attr("href") == '#header') {
//           scrollto = 0;
//         }

//         $('html, body').animate({
//           scrollTop: scrollto
//         }, 1500, 'easeInOutExpo');

//         if ($(this).parents('.nav-menu').length) {
//           $('.nav-menu .active').removeClass('active');
//           $(this).closest('li').addClass('active');
//           $('.nav-menu').removeClass('nav-menu-active');
//           $('.nav-toggle').removeClass('nav-toggle-active');
//           $('.nav-toggle i').toggleClass('bx-x bx-menu');
//         }
//         return false;
//       }
//     }
//   });

// })(jQuery);


/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
  }
  
  function filterFunction() {
    var input, filter, ul, li, a, i;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    div = document.getElementById("myDropdown");
    a = div.getElementsByTagName("a");
    for (i = 0; i < a.length; i++) {
      txtValue = a[i].textContent || a[i].innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        a[i].style.display = "";
      } else {
        a[i].style.display = "none";
      }
    }
  } 