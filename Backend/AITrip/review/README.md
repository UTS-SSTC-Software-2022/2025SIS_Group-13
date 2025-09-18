# Review API Documentation

This document describes the RESTful API endpoints for the **Review** module in the AITrip project.

Base URL: `/reviews/`

---

## Fields

- **user**: (int) ID of the user who created the review
- **category**: (string) One of `"itinerary"`, `"poi"`, `"daily_schedule"`
- **itinerary**: (int | null) ID of the itinerary (if category is "itinerary")
- **poi**: (int | null) ID of the POI (if category is "poi")
- **feedback_text**: (string) The content of the review

---

## 🔍 GET `/reviews/`

Returns a list of all reviews.

### Example Response
```json
[
  {
    "id": 1,
    "user": 2,
    "category": "itinerary",
    "itinerary": 3,
    "poi": null,
    "feedback_text": "Great itinerary!"
  }
]
```

---

## POST `/reviews/`

Creates a new review.

### Example Request
```json
{
  "user": 2,
  "category": "poi",
  "poi": 5,
  "feedback_text": "The place was wonderful and clean!"
}
```

### Example Response
```json
{
  "id": 7,
  "user": 2,
  "category": "poi",
  "itinerary": null,
  "poi": 5,
  "feedback_text": "The place was wonderful and clean!"
}
```

---

## GET `/reviews/{id}/`

Retrieves a specific review by ID.

### Example Response
```json
{
  "id": 1,
  "user": 2,
  "category": "daily_schedule",
  "itinerary": null,
  "poi": null,
  "feedback_text": "Too packed schedule."
}
```

---

## PUT `/reviews/{id}/`

Updates a review completely.

### Example Request
```json
{
  "user": 2,
  "category": "itinerary",
  "itinerary": 3,
  "feedback_text": "Loved it! Very organized."
}
```

---

## PATCH `/reviews/{id}/`

Partially updates a review.

### Example Request
```json
{
  "feedback_text": "Updated comment!"
}
```

---

## DELETE `/reviews/{id}/`

Deletes a review.

### Example Response
```json
204 No Content
```

---

## Notes

- Make sure only one of `itinerary` or `poi` is filled depending on the category.
- `daily_schedule` category may not use either foreign key currently.