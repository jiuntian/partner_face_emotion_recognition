$(document).ready(function(){
    console.log('shhshs')
    $('form input').change(function () {
      $('form p').text(this.files[0].name + " selected");
    });
  });