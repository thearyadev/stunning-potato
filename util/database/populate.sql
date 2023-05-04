insert into
    actress (uuid, name_)
values
    ('9c2a5dce-c9d6-492b-bd6a-e6222ce3b1c2', 'Aaliyah Hadid'),
    ('2405603a-e027-4b2f-bc7d-c2dbee6aa1f1', 'Abella Danger'),
    ('7d135e99-53a9-4b7e-8c90-cd6a1c487ca8', 'Abigail Mac'),
    ('2bccd8f0-3c0c-4ac6-b06e-d076476cc42c', 'Adriana Chechik'),
    ('4ac8865e-da85-4b24-b13c-12bc7394eda2', 'Aidra Fox'),
    ('14e0b741-d0f9-4faf-922f-def577cede20', 'Alex Grey'),
    ('b6b7b419-e28b-4321-893a-913af0bab732', 'Alexis Fawx');



insert into
    rating (
        uuid,
        story,
        positions,
        pussy,
        shots,
        boobs,
        face,
        rearview
    )
values
    ('6eef76c9-e546-4f70-b4fd-059e1df29353', 1, 2, 10, 5, 2, 2, 2),
    ('75755fa3-fa84-433f-bdae-29f53c412cff', 2, 2, 10, 2, 8, 2, 2),
    ('ea29b24e-79aa-4dd9-a31d-cf8b0630b577', 2, 3, 10, 2, 2, 7, 2);

insert into
    film (
        uuid,
        title,
        duration,
        date_added,
        filename,
        watched,
        state,
        thumbnail,
        poster
    )
values
    (
        'a627b0eb-737f-4780-aacf-f23cdea106db',
        'Sex in the city!',
        '00:41:00',
        '2019-01-01',
        'sexinthecity.mp4',
        false,
        'COMPLETE',
        null,
        null
    ),
    (
        'eb3d1228-8d86-435e-a210-ba4fbf22da05',
        'Lacy Lennon Cum',
        '00:41:00',
        '2019-01-01',
        'lacylennoncum.mp4',
        false,
        'IN QUEUE',
        null,
        null
    ),
    (
        'e1f59ef7-0ad1-4d6b-b0c6-a8a9c0ca40ed',
        'Scarlet Skies Sex',
        '00:41:00',
        '2019-01-01',
        'scarletskiessex.mp4',
        true,
        'DOWNLOADING',
        null,
        null
    );

insert into
    film_actress_rating (film_uuid, actress_uuid, rating_uuid)
values
    (
        'a627b0eb-737f-4780-aacf-f23cdea106db',
        ARRAY ['b6b7b419-e28b-4321-893a-913af0bab732'::uuid, '9c2a5dce-c9d6-492b-bd6a-e6222ce3b1c2'::uuid],
        'ea29b24e-79aa-4dd9-a31d-cf8b0630b577'
    ),
    (
        'eb3d1228-8d86-435e-a210-ba4fbf22da05',
        ARRAY ['2bccd8f0-3c0c-4ac6-b06e-d076476cc42c'::uuid, 'b6b7b419-e28b-4321-893a-913af0bab732'::uuid],
        '75755fa3-fa84-433f-bdae-29f53c412cff'
    ),
    (
        'e1f59ef7-0ad1-4d6b-b0c6-a8a9c0ca40ed',
        ARRAY ['2405603a-e027-4b2f-bc7d-c2dbee6aa1f1'::uuid, '14e0b741-d0f9-4faf-922f-def577cede20'::uuid, '7d135e99-53a9-4b7e-8c90-cd6a1c487ca8'::uuid],
        '6eef76c9-e546-4f70-b4fd-059e1df29353'
    );