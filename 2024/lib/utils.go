package lib

type Number interface {
	~int | ~int8 | ~int16 | ~int32 | ~int64 |
	~uint | ~uint8 | ~uint16 | ~uint32 | ~uint64 |
	~float32 | ~float64
}

func QuickSort[T Number](array []T) []T {
	if len(array) <= 1 {
		return array
	}

	pivot := array[len(array) / 2]
	left := []T{}
	middle := []T{}
	right := []T{}

	for _, x := range array {
		if x < pivot {
			left = append(left, x)
		} else if x == pivot {
			middle = append(middle, x)
		} else {
			right = append(right, x)
		}
	}

	left = QuickSort(left)
	right = QuickSort(right)

	return append(append(left, middle...), right...)
}

func Abs[T Number](number T) T {
	if number < 0 {
		return -number
	}
	return number
}
