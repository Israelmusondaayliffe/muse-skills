# Reference Inheritance Template

| Reference ID | Role | May inherit | Must not inherit | Evidence |
| --- | --- | --- | --- | --- |
| `@char_...` | Identity | Face, build, durable state | Unapproved camera, grade, or pose | Asset review ID |
| `@loc_...` | Geography | Space, materials, anchors, light logic | Starting composition unless requested | Location review ID |
| `@prop_...` | Object state | Shape, material, scale, state | Unrelated surrounding scene | Prop review ID |

Before a prompt handoff, remove every reference that is not active in the current shot. Name the role of every retained reference so it cannot silently control the wrong property.
