document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('sidebar-toggle').onclick = function () {
        var sidebar = document.getElementById('sidebar');
        var content = document.getElementById('page-content');
        sidebar.classList.toggle('collapsed');
        content.classList.toggle('expanded');
    };
});
