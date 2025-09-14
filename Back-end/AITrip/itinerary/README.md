**Base URL:** `/api/itinerary/`
 **Authentication:** JWT Bearer Token required

```
Authorization: Bearer <access_token>
```

**Response format:**
 All responses follow this structure:

```
{
  "success": 1,        // 1 for success, 0 for error
  "msg": "Operation successful",
  "data": {}           // Payload
}
```

**Filtering:**
 All model fields are filterable via query parameters, e.g.:

```
GET /api/itinerary/pois/?name=Osaka%20Castle
```

**Pagination (Optional):**

- Query parameters for pagination:

| Parameter   | Type | Default  | Description                                                |
| ----------- | ---- | -------- | ---------------------------------------------------------- |
| `page`      | int  | optional | Page number. If omitted, returns all results.              |
| `page_size` | int  | optional | Items per page (max 100). Only used if `page` is provided. |

- **Behavior**: If `page` is not passed, the API returns **all records** without pagination.

------

## **1. Itineraries**

| Method | URL                                          | Description                                             |
| ------ | -------------------------------------------- | ------------------------------------------------------- |
| GET    | `/api/itinerary/itineraries/`                | List itineraries (paginated only if `page` is provided) |
| POST   | `/api/itinerary/itineraries/`                | Create a new itinerary                                  |
| GET    | `/api/itinerary/itineraries/{itinerary_id}/` | Retrieve an itinerary                                   |
| PUT    | `/api/itinerary/itineraries/{itinerary_id}/` | Update an itinerary                                     |
| PATCH  | `/api/itinerary/itineraries/{itinerary_id}/` | Partially update an itinerary                           |
| DELETE | `/api/itinerary/itineraries/{itinerary_id}/` | Delete an itinerary                                     |

### Request Body (POST/PUT/PATCH)

| Field   | Type   | Required | Description     |
| ------- | ------ | -------- | --------------- |
| `title` | string | ✅ Yes    | Itinerary title |

> `user` is automatically set to the authenticated user.

### Response Example (List with Pagination)

```
{
  "success": 1,
  "msg": "Operation successful",
  "data": {
    "count": 12,
    "next": "/api/itinerary/itineraries/?page=2",
    "previous": null,
    "results": [
      {
        "itinerary_id": 1,
        "title": "Japan Trip",
        "user": 3,
        "daily_schedules": [],
        "create_time": "2025-09-14T08:00:00Z",
        "update_time": "2025-09-14T08:30:00Z"
      }
    ]
  }
}
```

### Response Example (List without Pagination)

```
{
  "success": 1,
  "msg": "Operation successful",
  "data": [
    {
      "itinerary_id": 1,
      "title": "Japan Trip",
      "user": 3,
      "daily_schedules": [],
      "create_time": "2025-09-14T08:00:00Z",
      "update_time": "2025-09-14T08:30:00Z"
    },
    {
      "itinerary_id": 2,
      "title": "Kyoto Weekend",
      "user": 3,
      "daily_schedules": [],
      "create_time": "2025-09-12T10:00:00Z",
      "update_time": "2025-09-12T10:30:00Z"
    }
  ]
}
```

------

## **2. Daily Schedules**

| Method | URL                                             | Description                                            |
| ------ | ----------------------------------------------- | ------------------------------------------------------ |
| GET    | `/api/itinerary/daily-schedules/`               | List daily schedules (paginated if `page` is provided) |
| POST   | `/api/itinerary/daily-schedules/`               | Create a daily schedule                                |
| GET    | `/api/itinerary/daily-schedules/{schedule_id}/` | Retrieve a daily schedule                              |
| PUT    | `/api/itinerary/daily-schedules/{schedule_id}/` | Update a daily schedule                                |
| PATCH  | `/api/itinerary/daily-schedules/{schedule_id}/` | Partially update a daily schedule                      |
| DELETE | `/api/itinerary/daily-schedules/{schedule_id}/` | Delete a daily schedule                                |

### Request Body (POST/PUT/PATCH)

| Field        | Type    | Required | Description             |
| ------------ | ------- | -------- | ----------------------- |
| `itinerary`  | integer | ✅ Yes    | Related itinerary ID    |
| `day_number` | integer | ✅ Yes    | Day number in itinerary |
| `start_time` | time    | ✅ Yes    | Start time (HH:MM:SS)   |
| `end_time`   | time    | ✅ Yes    | End time (HH:MM:SS)     |
| `summary`    | string  | ❌ No     | Daily schedule summary  |

------

## **3. Points of Interest (POIs)**

| Method | URL                             | Description                                 |
| ------ | ------------------------------- | ------------------------------------------- |
| GET    | `/api/itinerary/pois/`          | List POIs (paginated if `page` is provided) |
| POST   | `/api/itinerary/pois/`          | Create a POI                                |
| GET    | `/api/itinerary/pois/{poi_id}/` | Retrieve a POI                              |
| PUT    | `/api/itinerary/pois/{poi_id}/` | Update a POI                                |
| PATCH  | `/api/itinerary/pois/{poi_id}/` | Partially update a POI                      |
| DELETE | `/api/itinerary/pois/{poi_id}/` | Delete a POI                                |

### Request Body (POST/PUT/PATCH)

| Field             | Type    | Required | Description                 |
| ----------------- | ------- | -------- | --------------------------- |
| `schedule`        | integer | ✅ Yes    | Related daily schedule ID   |
| `name`            | string  | ✅ Yes    | POI name                    |
| `description`     | string  | ❌ No     | Description                 |
| `category`        | string  | ❌ No     | Category                    |
| `location`        | string  | ❌ No     | Address                     |
| `target_audience` | string  | ❌ No     | Target audience             |
| `booking_link`    | string  | ❌ No     | Booking link                |
| `avg_duration`    | integer | ❌ No     | Average duration in minutes |
| `opening_hours`   | string  | ❌ No     | Opening hours               |
| `ticket_price`    | string  | ❌ No     | Ticket price                |
| `review_summary`  | string  | ❌ No     | Review summary              |
| `review_source`   | string  | ❌ No     | Review source               |
| `rating`          | decimal | ❌ No     | Rating (0.0–10.0)           |

------

## **4. Error Response Example**

```
{
  "success": 0,
  "msg": "Operation failed",
  "data": {
    "name": ["This field may not be blank."]
  }
}
```

------

## 