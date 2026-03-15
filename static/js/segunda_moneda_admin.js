document.addEventListener('DOMContentLoaded', function () {
    var checkbox = document.getElementById('id_habilitar_segunda_moneda');

    function toggleSegundaMoneda() {
        var enabled = checkbox ? checkbox.checked : false;
        var selectors = ['.field-segunda_moneda', '.field-tipo_de_cambio'];
        selectors.forEach(function (sel) {
            var row = document.querySelector(sel);
            if (row) {
                row.style.opacity = enabled ? '1' : '0.45';
                row.style.pointerEvents = enabled ? 'auto' : 'none';
                row.style.transition = 'opacity 0.2s';
            }
        });
    }

    if (checkbox) {
        checkbox.addEventListener('change', toggleSegundaMoneda);
        toggleSegundaMoneda();
    }
});
