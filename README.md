# Наработка бота для парсинга почты
Бот парсит общую почту, а конкретно письма из сервиса "Яндекс.Бизнес", рендерит их в изображение и отправляет в чат Телеграма нужным специалистам, которые занимаются проектом. 
Информацию о специалистах и проектах, за которые он ответственен, бот берет из базы данных. Даже если в одном письме указано несколько проектов, над которыми работают разные специалисты, бот отправит это письмо им одновременно.