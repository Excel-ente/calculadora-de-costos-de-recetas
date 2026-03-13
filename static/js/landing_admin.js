document.addEventListener('DOMContentLoaded', function () {
    const sectionHero = document.querySelector('#id_section_hero');
    const sectionCategory = document.querySelector('#id_section_category');
    const sectionGallery = document.querySelector('#id_section_gallery');
    const aboutUs = document.querySelector('#id_about_us');
    const testimonials = document.querySelector('#id_testimonials');
    const features = document.querySelector('#id_features');
    const ctaSection = document.querySelector('#id_cta_section');
    const newsletter = document.querySelector('#id_newsletter');

    const fieldsets = {
        sectionHero: document.querySelector('.module.collapse:first-of-type'),
        sectionCategory: document.querySelector('.module.collapse:nth-of-type(2)'),
        sectionGallery: document.querySelector('.module.collapse:nth-of-type(3)'),
        aboutUs: document.querySelector('.module.collapse:nth-of-type(4)'),
        testimonials: document.querySelector('.module.collapse:nth-of-type(5)'),
        features: document.querySelector('.module.collapse:nth-of-type(6)'),
        ctaSection: document.querySelector('.module.collapse:nth-of-type(7)'),
        newsletter: document.querySelector('.module.collapse:nth-of-type(8)')
    };

    // Función para ocultar/mostrar fieldsets
    function toggleFieldset(section, fieldset) {
        if (section.checked) {
            fieldset.style.display = 'block';
        } else {
            fieldset.style.display = 'none';
        }
    }

    // Inicializa la visibilidad al cargar la página
    toggleFieldset(sectionHero, fieldsets.sectionHero);
    toggleFieldset(sectionCategory, fieldsets.sectionCategory);
    toggleFieldset(sectionGallery, fieldsets.sectionGallery);
    toggleFieldset(aboutUs, fieldsets.aboutUs);
    toggleFieldset(testimonials, fieldsets.testimonials);
    toggleFieldset(features, fieldsets.features);
    toggleFieldset(ctaSection, fieldsets.ctaSection);
    toggleFieldset(newsletter, fieldsets.newsletter);

    // Añadir eventos para cada checkbox
    sectionHero.addEventListener('change', function () {
        toggleFieldset(sectionHero, fieldsets.sectionHero);
    });

    sectionCategory.addEventListener('change', function () {
        toggleFieldset(sectionCategory, fieldsets.sectionCategory);
    });

    sectionGallery.addEventListener('change', function () {
        toggleFieldset(sectionGallery, fieldsets.sectionGallery);
    });

    aboutUs.addEventListener('change', function () {
        toggleFieldset(aboutUs, fieldsets.aboutUs);
    });

    testimonials.addEventListener('change', function () {
        toggleFieldset(testimonials, fieldsets.testimonials);
    });

    features.addEventListener('change', function () {
        toggleFieldset(features, fieldsets.features);
    });

    ctaSection.addEventListener('change', function () {
        toggleFieldset(ctaSection, fieldsets.ctaSection);
    });

    newsletter.addEventListener('change', function () {
        toggleFieldset(newsletter, fieldsets.newsletter);
    });
});
