

// Contador para que desaparezcan los mensajes después de 3 segundos
// Wait for the document to be ready
<script>
  $(document).ready(function () {
    // Find all elements with the class "alert" that have the class "alert-dismissible"
    // and start the timeout to hide them after 5 seconds
    $(".alert.alert-dismissible").each(function () {
      var alertId = $(this).attr("id");
      setTimeout(function () {
        $("#" + alertId).alert("close");
      }, 3000); // 3000 milliseconds (3 seconds)
    });
  });
</script>
