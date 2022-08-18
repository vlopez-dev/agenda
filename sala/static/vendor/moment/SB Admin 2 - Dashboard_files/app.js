




function fire(){
Swal.fire({
      title: 'Are you sure?',
      text: "You won't be able to revert this!",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
      if (result.isConfirmed) {
        Swal.fire(
          'Deleted!',
          'Your file has been deleted.',
          'success'
        )
      }
    })
    }

    $(function () {
        $('#datetimepicker12').datetimepicker({
            inline: true,
            sideBySide: true,
            format: 'DD.MM.YYYY' /*remove this line if you want to use time as well */
        });
    });
