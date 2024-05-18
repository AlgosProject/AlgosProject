db.dropDatabase("algos_project")

db = db.getSiblingDB("algos_project")

const u1 = ObjectId();
const u2 = ObjectId();
const u3 = ObjectId();
const u4 = ObjectId();
const p1 = ObjectId();
const p2 = ObjectId();
const p3 = ObjectId();
const c1 = ObjectId();
const g1 = ObjectId();
const t1 = ObjectId();
const t2 = ObjectId();

db.tags.insertMany([{
    _id: t1,
    name: "cats",
    post_ids: [p3]
}, {
    _id: t2,
    name: "dogs",
    post_ids: [p2]
}])


db.users.insertMany([
    {
        _id: u1,
        username: "Ryan",
        password: "$2b$12$HXHNjc6DGlpfAjz23fqmJOZBVrhoSVjxcU2hXifvSauSwg8ocUVJu",
        privacy_control: 2,
        name: "Ryan Rick",
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
        name: "Rul vir",
        friends: [
            {friend_id: u1, affinity: 2},
            {friend_id: u4, affinity: 4}
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
        name: "mocha cat",
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
        username: "Marian",
        password: "$2b$12$HXHNjc6DGlpfAjz23fqmJOZBVrhoSVjxcU2hXifvSauSwg8ocUVJu",
        privacy_control: 7,
        name: "Mira cat",
        friends: [
            {friend_id: u1, affinity: 4},
            {friend_id: u2, affinity: 4},
            {friend_id: u3, affinity: 4}
        ],
        seen: [],
        tags: [
            {tag_id: t1, affinity: 3},
            {tag_id: t2, affinity: 2}
        ]
    }

])


db.posts.insertMany([
    {
        _id: p1,
        user_id: u1,
        likes: [],
        photo_url: "",
        text: "My first post??!!",
        comments: [c1],
        tags: []
    },
    {
        _id: p2,
        user_id: u2,
        likes: [],
        photo_url: "",
        text: "Dogs are better than cats",
        comments: [],
        tags: []
    },
    {
        _id: p3,
        user_id: u3,
        likes: [],
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
        user_id: u3,
        text: "Change your password silly"
    }
])


db.groups.insertMany([
    {
        _id: g1,
        users: [u1, u2, u3]
    }
])

db.messages.insertMany([
    {
        group_id: g1,
        user_id: u1,
        text: "I made this chat to explain how bad this semester is going"
    },
    {
        group_id: g1,
        user_id: u2,
        text: "Same for me"
    }
])