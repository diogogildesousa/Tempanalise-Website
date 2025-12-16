document.addEventListener('DOMContentLoaded', function () {

    /* ========================================= */
    /* Lógica do Menu Hamburger */
    /* ========================================= */
    const btn = document.getElementById('hamburgerBtn');
    const navLinks = document.querySelector('header nav .nav-links');

    if (btn && navLinks) {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            navLinks.classList.toggle('show');
            btn.classList.toggle('open');
            document.body.classList.toggle('no-scroll');
            // AQUI ESTÁ A LÓGICA CORRIGIDA
            if (navLinks.classList.contains('show')) {
                navLinks.classList.add('mobile-menu-overlay');
            } else {
                navLinks.classList.remove('mobile-menu-overlay');
            }
        });

        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                if (navLinks.classList.contains('show')) {
                    navLinks.classList.remove('show');
                    btn.classList.remove('open');
                    document.body.classList.remove('no-scroll');
                    // AQUI ESTÁ A LÓGICA CORRIGIDA
                    navLinks.classList.remove('mobile-menu-overlay');
                }
            });
        });

        document.addEventListener('click', function (ev) {
            if (!navLinks.classList.contains('show')) return;
            const target = ev.target;
            if (!navLinks.contains(target) && target !== btn && !btn.contains(target)) {
                navLinks.classList.remove('show');
                btn.classList.remove('open');
                document.body.classList.remove('no-scroll');
                // AQUI ESTÁ A LÓGICA CORRIGIDA
                navLinks.classList.remove('mobile-menu-overlay');
            }
        });
    }

    /* ========================================= */
    /* Lógica do Modo Claro/Escuro (Com Animação) */
    /* ========================================= */
    const themeToggleBtn = document.getElementById('theme-toggle');

    if (themeToggleBtn) {
        // Função para aplicar o tema com base na classe 'dark-mode'
        const applyTheme = (isDarkMode) => {
            if (isDarkMode) {
                document.body.classList.add('dark-mode');
                themeToggleBtn.classList.add('dark-mode');
            } else {
                document.body.classList.remove('dark-mode');
                themeToggleBtn.classList.remove('dark-mode');
            }
        };

        // Carregar a preferência salva no localStorage
        const savedTheme = localStorage.getItem('theme');
        const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;

        // Aplicar o tema inicial
        if (savedTheme === 'dark') {
            applyTheme(true);
        } else if (savedTheme === 'light') {
            applyTheme(false);
        } else if (prefersDark) {
            applyTheme(true);
        } else {
            applyTheme(false);
        }

        // Adicionar o event listener para alternar o tema
        themeToggleBtn.addEventListener('click', () => {
            const isDarkMode = document.body.classList.toggle('dark-mode');
            themeToggleBtn.classList.toggle('dark-mode');
            const themeToSave = isDarkMode ? 'dark' : 'light';
            localStorage.setItem('theme', themeToSave);
        });
    }

});