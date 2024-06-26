db.dropDatabase("algos_project")

db = db.getSiblingDB("algos_project")

const u1 = ObjectId();
const u2 = ObjectId();
const u3 = ObjectId();
const u4 = ObjectId();
const u5 = ObjectId();
const u6 = ObjectId();
const u7 = ObjectId();
const u8 = ObjectId();
const p1 = ObjectId();
const p2 = ObjectId();
const p3 = ObjectId();
const c1 = ObjectId();
const g1 = ObjectId();
const g2 = ObjectId();
const g3 = ObjectId();
const g4 = ObjectId();
const t1 = ObjectId();
const t2 = ObjectId();
const t3 = ObjectId();
const t4 = ObjectId();
const t5 = ObjectId();
const t6 = ObjectId();

db.tags.insertMany([{
    _id: t1,
    name: "cats",
    post_ids: [p3]
}, {
    _id: t2,
    name: "dogs",
    post_ids: [p2]
}, {
    _id: t3,
    name: "dragons",
    post_ids: []
}, {
    _id: t4,
    name: "school",
    post_ids: []
}, {
    _id: t5,
    name: "productivity",
    post_ids: []
}, {
    _id: t6,
    name: "foxes",
    post_ids: []
}])


db.users.insertMany([
    {
        _id: u1,
        username: "u1",
        password: "$2b$12$HXHNjc6DGlpfAjz23fqmJOZBVrhoSVjxcU2hXifvSauSwg8ocUVJu",
        privacy_control: 2,
        name: "u1",
        friends: [
            {friend_id: u2, affinity: 8},
            {friend_id: u3, affinity: 1},
            {friend_id: u4, affinity: 4}
        ],
        seen: [],
        tags: [
            {tag_id: t1, affinity: 4}
        ]
    },
    {
        _id: u2,
        username: "Rul",
        password: "$2b$12$HXHNjc6DGlpfAjz23fqmJOZBVrhoSVjxcU2hXifvSauSwg8ocUVJu",
        privacy_control: 1,
        name: "u2",
        friends: [
            {friend_id: u1, affinity: 2},
            {friend_id: u4, affinity: 4},
            {friend_id: u5, affinity: 4}
        ],
        seen: [],
        tags: [
            {tag_id: t2, affinity: 4}
        ]
    },
    {
        _id: u3,
        username: "mocha",
        password: "$2b$12$HXHNjc6DGlpfAjz23fqmJOZBVrhoSVjxcU2hXifvSauSwg8ocUVJu",
        privacy_control: 7,
        name: "u3",
        friends: [
            {friend_id: u1, affinity: 4},
            {friend_id: u4, affinity: 4}
        ],
        seen: [],
        tags: [
            {tag_id: t1, affinity: 3},
            {tag_id: t2, affinity: 2}
        ]
    },
    {
        _id: u4,
        username: "u4",
        password: "$2b$12$HXHNjc6DGlpfAjz23fqmJOZBVrhoSVjxcU2hXifvSauSwg8ocUVJu",
        privacy_control: 7,
        name: "u4",
        friends: [
            {friend_id: u1, affinity: 4},
            {friend_id: u2, affinity: 4},
            {friend_id: u3, affinity: 4}
        ],
        seen: [],
        tags: [
            {tag_id: t1, affinity: 3},
            {tag_id: t2, affinity: 2},
            {tag_id: t3, affinity: 10},
            {tag_id: t5, affinity: 4},
            {tag_id: t4, affinity: -8},
            {tag_id: t6, affinity: 10}
        ]
    },
    {
        _id: u5,
        username: "u5",
        password: "$2b$12$HXHNjc6DGlpfAjz23fqmJOZBVrhoSVjxcU2hXifvSauSwg8ocUVJu",
        privacy_control: 2,
        name: "u5",
        friends: [
            {friend_id: u2, affinity: 4},
            {friend_id: u6, affinity: 4}
        ],
        seen: [],
        tags: [
            {tag_id: t1, affinity: 4}
        ]
    },
    {
        _id: u6,
        username: "u6",
        password: "$2b$12$HXHNjc6DGlpfAjz23fqmJOZBVrhoSVjxcU2hXifvSauSwg8ocUVJu",
        privacy_control: 2,
        name: "u6",
        friends: [
            {friend_id: u5, affinity: 4},
            {friend_id: u7, affinity: 4}
        ],
        seen: [],
        tags: [
            {tag_id: t1, affinity: 4}
        ]
    },
    {
        _id: u7,
        username: "u7",
        password: "$2b$12$HXHNjc6DGlpfAjz23fqmJOZBVrhoSVjxcU2hXifvSauSwg8ocUVJu",
        privacy_control: 2,
        name: "u7",
        friends: [
            {friend_id: u6, affinity: 4},
            {friend_id: u8, affinity: 4}
        ],
        seen: [],
        tags: [
            {tag_id: t1, affinity: 4}
        ]
    },
    {
        _id: u8,
        username: "u8",
        password: "$2b$12$HXHNjc6DGlpfAjz23fqmJOZBVrhoSVjxcU2hXifvSauSwg8ocUVJu",
        privacy_control: 2,
        name: "u8",
        friends: [
            {friend_id: u7, affinity: 4}
        ],
        seen: [],
        tags: [
            {tag_id: t1, affinity: 4}
        ]
    },

])


db.posts.insertMany([
    {
        _id: p1,
        user_id: u1,
        likes: [],
        dislikes: [],
        photo_url: "",
        text: "My first post??!!",
        comments: [c1],
        tags: []
    },
    {
        _id: p2,
        user_id: u2,
        likes: [],
        dislikes: [],
        photo_url: "",
        text: "Dogs are better than cats",
        comments: [],
        tags: []
    },
    {
        _id: p3,
        user_id: u3,
        likes: [],
        dislikes: [],
        photo_url: "",
        text: "Cats are great",
        comments: [],
        tags: [t1]
    }
])

db.comments.insertMany([
    {
        _id: c1,
        user_id: u2,
        post_id: p1,
        text: "Is it though?"
    }
])

db.notifications.insertMany([
    {
        user_id: u1,  //** Owner of Notif
        author_id: u3, //** Who created it
        origin_id: g4, //** Where is it from
        type: "chat"
    },
    {
        user_id: u1,
        author_id: u8, //** User if of Origin
        origin_id: null,
        type: "friend_request"
    }
])


db.groups.insertMany([
    {
        _id: g1,
        users: [u1, u2, u3],
        type: "community"
    },
    {
        _id: g2,
        users: [u1, u2, u3],
        type: "community"
    },
    {
        _id: g3,
        users: [u1, u2],
        type: "chat"
    },
    {
        _id: g4,
        users: [u1, u3],
        type: "chat"
    }

])


db.messages.insertMany([
    {
        group_id: g2,
        user_id: u1,
        text: "I made this chat to explain how bad this semester is going"
    },
    {
        group_id: g2,
        user_id: u2,
        text: "Same for me"
    },
    {
        group_id: g3,
        user_id: u2,
        text: "Hi"
    },
    {
        group_id: g3,
        user_id: u1,
        text: "I hate you but not too strongly"
    },
    {
        group_id: g4,
        user_id: u1,
        text: "Hello my dear friend of all life"
    }
])