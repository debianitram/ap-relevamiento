// Configuration Size Windows
var windowResizeHandler = function() {
    window_height = $(window).height();
    columns_view = $('#columns-view').height();
    $('#down').height(window_height - columns_view - 50);
}

var Init = function(){
    windowResizeHandler();
    FormLampara = $('#form-lampara');
    Modal = $('.modal');

    $('#add_lampara').on('click',
        function(){
            Modal.modal('show');
    });

    FormLampara.on('submit',
        function(event){
            event.preventDefault();
            $.post('/form-lampara',
                   {tipo: FormLampara.find('input[name="tipo"]').val(),
                    estado: FormLampara.find('input[name="estado"]').val(),
                    modelo_artefacto: FormLampara.find('input[name="modelo_artefacto"]').val(),
                    potencia: FormLampara.find('input[name="potencia"]').val(),
                   },
                   function(data){
                        console.log(data);
                        Modal.modal('hide');
                   }
            )
        }
    )
}

// Resize maps where resize window.
window.onload = Init;
$(window).on('resize', windowResizeHandler);