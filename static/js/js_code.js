// $(document).ready(function() {
//      $('form').on('submit', function(event) {
//        $.ajax({
//           data : {
//              buttonAnswer : $('#buttonAnswer').val(),
//                  },
//              type : 'POST',
//              url : '/'
//             })
//         ;
//       });
//       event.preventDefault();
//       });



$(document).ready(function(){
    $("#send").click(function(){
        parent.$("#frame2").contents().find("#target").html($("#mydata").val());
    });
});


function myFunction() {
  alert("Hello! I am an alert box!");
}