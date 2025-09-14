## **General Information**

- **Authentication**: JWT Token required

  ```
  Authorization: Bearer <access_token>
  ```

- **Response Format**: JSON

- **Base URL**: `/api/itinerary/`

- **Pagination**

  - Default page size: 5 items per page

  - Can be customized with query parameters:

    | Parameter   | Type | Default | Description                            |
    | ----------- | ---- | ------- | -------------------------------------- |
    | `page`      | int  | 1       | Page number                            |
    | `page_size` | int  | 5       | Number of items per page (maximum 100) |

- **Filtering**: All model fields are filterable.
   Example:

  ```
  GET /api/itinerary/pois/?name=Osaka%20Castle
  ```

------

## **1. Itineraries Management**

| Method     | URL                                | Description                   |
| ---------- | ---------------------------------- | ----------------------------- |
| **GET**    | `/api/itinerary/itineraries/`      | List itineraries (paginated)  |
| **POST**   | `/api/itinerary/itineraries/`      | Create a new itinerary        |
| **GET**    | `/api/itinerary/itineraries/{id}/` | Retrieve itinerary details    |
| **PUT**    | `/api/itinerary/itineraries/{id}/` | Update an itinerary           |
| **PATCH**  | `/api/itinerary/itineraries/{id}/` | Partially update an itinerary |
| **DELETE** | `/api/itinerary/itineraries/{id}/` | Delete an itinerary           |

### 1.1 Request Parameters (POST / PUT / PATCH)

| Field         | Type   | Required | Description             |
| ------------- | ------ | -------- | ----------------------- |
| `name`        | string | ✅ Yes    | Itinerary name          |
| `start_date`  | date   | ✅ Yes    | Start date `YYYY-MM-DD` |
| `end_date`    | date   | ✅ Yes    | End date `YYYY-MM-DD`   |
| `description` | string | ❌ No     | Description             |

> The `user` field is automatically set to the current authenticated user.

------

### 1.2 Response Example (Paginated List)

```
{
  "count": 12,
  "next": "/api/itinerary/itineraries/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Japan Trip",
      "start_date": "2025-09-20",
      "end_date": "2025-09-30",
      "description": "Tokyo-Osaka-Kyoto 10-day tour",
      "user": 3,
      "create_time": "2025-09-14T08:00:00Z",
      "update_time": "2025-09-14T08:30:00Z"
    }
  ]
}
```

### 1.3 Query Examples

- Filter itineraries by name:

```
GET /api/itinerary/itineraries/?name=Japan%20Trip
```

- Second page with 10 items per page:

```
GET /api/itinerary/itineraries/?page=2&page_size=10
```

------

## **2. Daily Schedule Management**

| Method     | URL                                    | Description                       |
| ---------- | -------------------------------------- | --------------------------------- |
| **GET**    | `/api/itinerary/daily-schedules/`      | List daily schedules (paginated)  |
| **POST**   | `/api/itinerary/daily-schedules/`      | Create a daily schedule           |
| **GET**    | `/api/itinerary/daily-schedules/{id}/` | Retrieve a daily schedule         |
| **PUT**    | `/api/itinerary/daily-schedules/{id}/` | Update a daily schedule           |
| **PATCH**  | `/api/itinerary/daily-schedules/{id}/` | Partially update a daily schedule |
| **DELETE** | `/api/itinerary/daily-schedules/{id}/` | Delete a daily schedule           |

### 2.1 Request Parameters

| Field       | Type    | Required | Description          |
| ----------- | ------- | -------- | -------------------- |
| `itinerary` | integer | ✅ Yes    | Related itinerary ID |
| `date`      | date    | ✅ Yes    | Date `YYYY-MM-DD`    |
| `notes`     | string  | ❌ No     | Notes                |

------

### 2.2 Response Example (Paginated)

```
{
  "count": 20,
  "next": "/api/itinerary/daily-schedules/?page=2",
  "previous": null,
  "results": [
    {
      "id": 12,
      "itinerary": 1,
      "date": "2025-09-21",
      "notes": "Kyoto day trip",
      "pois": [
        {
          "id": 5,
          "name": "Fushimi Inari Shrine",
          "location": "Kyoto",
          "description": "Famous shrine with thousands of torii gates"
        }
      ],
      "create_time": "2025-09-14T08:10:00Z",
      "update_time": "2025-09-14T08:15:00Z"
    }
  ]
}
```

### 2.3 Query Examples

- Daily schedules for itinerary `id=1`:

```
GET /api/itinerary/daily-schedules/?itinerary=1
```

- Daily schedules for a specific date:

```
GET /api/itinerary/daily-schedules/?date=2025-09-21
```

------

## **3. Points of Interest (POIs) Management**

| Method     | URL                         | Description            |
| ---------- | --------------------------- | ---------------------- |
| **GET**    | `/api/itinerary/pois/`      | List POIs (paginated)  |
| **POST**   | `/api/itinerary/pois/`      | Create a POI           |
| **GET**    | `/api/itinerary/pois/{id}/` | Retrieve a POI         |
| **PUT**    | `/api/itinerary/pois/{id}/` | Update a POI           |
| **PATCH**  | `/api/itinerary/pois/{id}/` | Partially update a POI |
| **DELETE** | `/api/itinerary/pois/{id}/` | Delete a POI           |

### 3.1 Request Parameters

| Field            | Type    | Required | Description               |
| ---------------- | ------- | -------- | ------------------------- |
| `daily_schedule` | integer | ✅ Yes    | Related daily schedule ID |
| `name`           | string  | ✅ Yes    | POI name                  |
| `location`       | string  | ❌ No     | Address                   |
| `description`    | string  | ❌ No     | Description               |

------

### 3.2 Response Example (Paginated)

```
{
  "count": 15,
  "next": "/api/itinerary/pois/?page=2",
  "previous": null,
  "results": [
    {
      "id": 8,
      "daily_schedule": 12,
      "name": "Osaka Castle",
      "location": "Chuo Ward, Osaka",
      "description": "Famous historic landmark",
      "create_time": "2025-09-14T09:00:00Z",
      "update_time": "2025-09-14T09:05:00Z"
    }
  ]
}
```

### 3.3 Query Examples

- All POIs for daily schedule `id=12`:

```
GET /api/itinerary/pois/?daily_schedule=12
```

- Filter by POI name:

```
GET /api/itinerary/pois/?name=Osaka%20Castle
```

------

## **4. Error Response Format**

```
{
  "code": 400,
  "message": "Validation failed",
  "details": {
    "name": ["This field may not be blank."]
  }
}
```

------

## 