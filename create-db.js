db.dropDatabase("algos_project")

db = db.getSiblingDB("algos_project")

const u1 = ObjectId();
const u2 = ObjectId();
const u3 = ObjectId();
const p1 = ObjectId();
const p2 = ObjectId();
const c1 = ObjectId();
const g1 = ObjectId();
const t1 = ObjectId();
const t2 = ObjectId();

db.tags.insertMany([{
    _id: t1,
    name: "cats",
    post_ids: []
}, {
    _id: t2,
    name: "dogs",
    post_ids: []
}])


db.users.insertMany([
    {
        _id: u1,
        username: "Ryan",
        password: "dat",
        privacy_control: 2,
        name: "Ryan Rick",
        friends: [],
        seen: [],
        tags: {
            tag_id: t1,
            affinity: 4
        }
    },
    {
        _id: u2,
        username: "Rul",
        password: "pat",
        privacy_control: 1,
        name: "Rul vir",
        friends: [],
        seen: [],
        tags: {}
    },
    {
        _id: u3,
        username: "mocha",
        password: "cat",
        privacy_control: 7,
        name: "mocha cat",
        friends: [],
        seen: [],
        tags: {}
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
        text: "is it though?",
        comments: [],
        tags: []
    }
])

db.comments.insertMany([
    {
        _id: c1,
        user_id: u2,
        post_id: p2
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
        content: "I made this chat to explain how bad this semester is going"
    },
    {
        group_id: g1,
        user_id: u2,
        content: "Same for me"
    }
])