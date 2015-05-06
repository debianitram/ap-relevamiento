// Configuration Size Windows
var windowResizeHandler = function() {
    window_height = $(window).height();
    columns_view = $('#columns-view').height();
    $('#down').height(window_height - columns_view - 150);
}

var ProcessLampara = function(){
    FormLampara = $('#form-lampara');
    Modal = $('.modal');

    FormLampara.on('submit',
        function(event){
            event.preventDefault();
            data = {};
            FormLampara.serializeArray().map(function(x){data[x.name] = x.value;});

            $.ajax({url: '/form-lampara', type: 'POST', data: data})
            
            .done(function(response, status, jqXHR){
                Modal.modal('hide');
                $('#ptos-luz').append(response);
                $('#__error').remove();
            })
            
            .fail(function (response, status, errorThrown){
                $('#__error').remove(); 
                FormLampara.prepend('<div id="__error" class="alert alert-danger">' 
                                    + response['responseText'] + 
                                    "</div>");
            });
        }
    )
}

var ProcessRelevamiento = function(){
    FormRelevamiento = $('#form-relevamiento');

    FormRelevamiento.on('submit',
        function(event){
            event.preventDefault();
            data = {};
            FormRelevamiento.serializeArray().map(function(x){data[x.name] = x.value;});

            $.post('/form-relevamiento',
                   data,
                   function(result){
                        // Success
                        console.log(result);
                   }
            )
        }
    );
}


var InfoExtra = function(){
    Sosten = $('#relevamiento_sosten');

    Sosten.on('change', function(e){
        
        $('.extras').find('input, input:checkbox, select').each(
            // reset value of widgets.
            function(pos, elem){
                if (elem.type == 'text') || (elem.type == 'select-one'){
                    elem.value = '';
                }
                if (elem.type == 'checkbox'){
                    elem.checked = false;
                }
            }
        );

        if (Sosten.val() == 'columna'){
            $('#madera-extra').hide();
            $('#sujecion-extra').hide();
            $('#columna-extra').show();
        }

        else if (Sosten.val() == 'madera'){
            $('#madera-extra').show();
            $('#sujecion-extra').show();
            $('#columna-extra').hide();
        }

        else if (Sosten.val() == 'ha') {
            $('#sujecion-extra').show();
            $('#madera-extra').hide();
            $('#columna-extra').hide();
        }

        else {
            $('#columna-extra').hide();
            $('#madera-extra').hide();
            $('#sujecion-extra').hide();
        }
    });
}


var Init = function(){
    windowResizeHandler();
    $('#add_lampara').on('click',
        function(){
            Modal.modal('show');
    });

    ProcessLampara();
    ProcessRelevamiento();
    InfoExtra();
}

// Resize maps where resize window.
window.onload = Init;
$(window).on('resize', windowResizeHandler);